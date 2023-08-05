from __future__ import (absolute_import, division, print_function, unicode_literals)

import logging
import os
import sys
import time
import traceback
from threading import Thread

import click

from .klass_convert import Convert
from .klass_operator import Operator
from .klass_queue import Queue
from .klass_str import Str
from .klass_yaml_config import YamlConfig


def __execute(logger, config, path, ctx):
    full_path = os.path.abspath(path)
    if not os.path.isfile(full_path):
        full_path = os.path.join(os.path.dirname(config), path)
    if not os.path.isfile(full_path):
        assert os.path.isfile(full_path), "The file [%s] not found" % full_path
    try:
        exec(open(full_path).read(), ctx)
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error('path: %s', full_path)
        sys.exit(-1)


def __load_connectors(logger, config, yaml, context):
    connectors = yaml.get_data()['connectors']
    for name, klass_path in connectors.items():
        params = yaml.get_data().get('params', {}).get(name, {})
        path, klass = klass_path.split('::')
        _ctx = context.copy()
        __execute(logger, config, path, _ctx)
        ctx_params = context.copy()
        ctx_params.update(params)
        context[name] = _ctx[klass](**ctx_params).get


def __get_jobs_priorities(logger, config, yaml, context, select, start, stop):
    select = [int(x) for x in Operator.split_and_flat(',', select)]
    jobs = yaml.get_data()['jobs']
    result = {}
    priorities = {}
    for job in jobs:
        if job.get('active', True):
            priority = job.get('priority', 1)
            if select and priority not in select:
                continue
            if start and priority < start:
                continue
            if stop and priority > stop:
                continue
            threads = job.get('threads', 1)
            priorities.setdefault(priority, 0)
            priorities[priority] += threads
            result.setdefault(priority, [])
            get_klass_method = job.pop('get')
            put_klass_method = job.pop('put')
            g_path, g_klass, g_method = get_klass_method.split('::')
            p_path, p_klass, p_method = put_klass_method.split('::')
            limit = job.get('limit', 0)
            offset = job.get('offset', 0)
            domain = job.get('domain', [])
            ctx = context.copy()
            __execute(logger, config, g_path, ctx)
            __execute(logger, config, p_path, ctx)
            job_ctx = context.copy()
            job_ctx.update(job)
            if limit:
                step = limit
                try:
                    count = ctx[g_klass](**job_ctx).count()
                except Exception as e:
                    logger.error(traceback.format_exc())
                    logger.error('path: %s', g_path)
                    sys.exit(-1)
                while offset < count:
                    job_ctx.update(dict(domain=domain, offset=offset, limit=limit))
                    offset += step
                    get_method = getattr(ctx[g_klass](**job_ctx), g_method)
                    put_method = getattr(ctx[p_klass](**job_ctx), p_method)
                    result[priority].append([priority, threads, get_method, put_method, job])
            else:
                job_ctx.update(dict(domain=domain, offset=0, limit=0))
                get_method = getattr(ctx[g_klass](**job_ctx), g_method)
                put_method = getattr(ctx[p_klass](**job_ctx), p_method)
                result[priority].append([priority, threads, get_method, put_method, job])
    return result, priorities


@click.command()
@click.option('--logfile', '-l',
              type=click.Path(file_okay=True, dir_okay=False, writable=True, readable=True, resolve_path=True,
                              allow_dash=True), required=False, )
@click.option('--config', '-c',
              type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True, readable=True,
                              resolve_path=True,
                              allow_dash=True), required=True, )
@click.option('--log-level', type=click.Choice(['debug', 'info', 'warning', 'error']), default='info', required=True, )
@click.option('--start', type=click.INT, default=False, )
@click.option('--stop', type=click.INT, default=False, )
@click.option('--select', '-s', type=click.STRING, nargs=1, multiple=True)
@click.pass_context
def cli_migrate(ctx, logfile, config, log_level, start, stop, select):
    """Command line for migrate"""
    time_start = time.time()
    os.chdir(os.path.dirname(config))
    yaml = YamlConfig(config)
    logger = logging.getLogger()
    logger.setLevel(log_level.upper())
    if logfile:
        handler = logging.FileHandler(logfile)
    else:
        handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    context = {
        'logfile': logfile,
        'logger': logger,
        'config': config,
        'yaml': yaml,
    }
    __load_connectors(logger, config, yaml, context)
    jobs, priorities = __get_jobs_priorities(logger, config, yaml, context, select, start, stop)

    queue = Queue()
    send_thread = Thread(target=queue.send, args=())
    send_thread.start()
    last_priority = 0
    len_priorities = len(priorities)
    for i, (queue_priority, queue_threads) in enumerate(priorities.items(), 1):
        logger.info('receiver: global advance %s/%s', i, len_priorities)
        len_queue_priority = len(jobs[queue_priority])
        queue.add(queue_priority, queue_threads, len_queue_priority)
        queue_threads = min([queue_threads, len_queue_priority])
        index = 0
        while index < len_queue_priority:
            logger.info('receiver: stage priority=%s %s-%s/%s', queue_priority, index, queue_threads + index,
                        len_queue_priority)
            tab = []
            for i in range(queue_threads):
                priority, threads, get_method, put_method, job = jobs[queue_priority][index]
                index += 1
                t = Thread(target=get_method, args=(put_method, queue, priority))
                t.start()
                tab.append(t)
            for t in tab:
                t.join()
            queue_threads = min([queue_threads, len(jobs[queue_priority][index:])])
        queue.push(queue_priority)
        while True:
            # wait for sender to finish with last_priority
            time.sleep(1)
            logger.debug('receiver: current prioritry=%s wait sender_index=%s >= last_priority=%s', queue_priority,
                         queue.sender_index, last_priority)
            if queue.sender_index >= last_priority:
                logger.info(
                    'receiver: after waiting for sender advance [last priority=%s], continue to priority after [%s]',
                    last_priority, queue_priority)
                break
        last_priority = queue_priority
    queue.stop()
    send_thread.join()
    logger.info('all: migration is completed [time=%s] [time=%s]',
                Str(Convert.time(time.time() - time_start, r=2), suffix='seconds'),
                Str(Convert.time(time.time() - time_start, to='M', r=2), suffix='minutes'))
