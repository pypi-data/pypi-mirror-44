# coding=utf-8
from __future__ import absolute_import, print_function

import contextlib
import functools
import multiprocessing
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool

import tqdm

from suanpan import utils

WORKERS = multiprocessing.cpu_count()
DEFAULT_PBAR_FORMAT = "{desc}: {n_fmt}/{total_fmt} |{bar}"
DEFAULT_PBAR_CONFIG = {"bar_format": DEFAULT_PBAR_FORMAT}


@contextlib.contextmanager
def multiThread(workers=None):
    workers = workers or WORKERS
    pool = ThreadPool(processes=workers)
    yield pool
    pool.close()


@contextlib.contextmanager
def multiProcess(workers=None):
    workers = workers or WORKERS
    pool = ProcessPool(processes=workers)
    yield pool
    pool.close()


def parsePbarConfig(pbar):
    if pbar is True:
        return utils.merge({}, DEFAULT_PBAR_CONFIG, {"desc": "Processing"})
    if isinstance(pbar, str):
        return utils.merge({}, DEFAULT_PBAR_CONFIG, {"desc": pbar})
    if pbar in (False, None):
        return utils.merge({}, DEFAULT_PBAR_CONFIG, {"disable": True})
    if isinstance(pbar, dict):
        return utils.merge({}, DEFAULT_PBAR_CONFIG, pbar)
    raise Exception("Invalid pbar config: bool | str | dict. but {}".format(pbar))


def pbarRunner(pbar, quantity=1):
    def _dec(runner):
        @functools.wraps(runner)
        def _runner(*args, **kwargs):
            result = runner(*args, **kwargs)
            pbar.update(quantity)
            return result

        return _runner

    return _dec


def starmapRunner(func):
    @functools.wraps(func)
    def runner(args):
        return func(*args)

    return runner


class StarmapRunner(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, args):
        return self.func(*args)


def getIterableLenForPbar(iterable, pbar=None, total=None):
    if pbar and total is None:
        iterable = list(iterable)
        total = len(iterable)
    return iterable, total


def map(func, iterable, chunksize=1, workers=None, pbar=None, thread=False, total=None):
    return list(
        imap(
            func,
            iterable,
            chunksize=chunksize,
            workers=workers,
            pbar=pbar,
            thread=thread,
            total=total,
        )
    )


def imap(
    func, iterable, chunksize=1, workers=None, pbar=None, thread=False, total=None
):
    items, total = getIterableLenForPbar(iterable, pbar=pbar, total=total)
    pbarConfig = parsePbarConfig(pbar)
    pbarConfig.update(total=total)
    poolClass = multiThread if thread else multiProcess
    with poolClass(workers) as pool:
        return tqdm.tqdm(pool.imap(func, items, chunksize=chunksize), **pbarConfig)


def starmap(
    func, iterable, chunksize=1, workers=None, pbar=None, thread=False, total=None
):
    return list(
        istarmap(
            func,
            iterable,
            chunksize=chunksize,
            workers=workers,
            pbar=pbar,
            thread=thread,
            total=total,
        )
    )


def istarmap(
    func, iterable, chunksize=1, workers=None, pbar=None, thread=False, total=None
):
    return imap(
        StarmapRunner(func),
        iterable,
        chunksize=chunksize,
        workers=workers,
        pbar=pbar,
        thread=thread,
        total=total,
    )


def run(func, args=(), kwds=None, thread=False, **kwargs):
    poolClass = multiThread if thread else multiProcess
    with poolClass(1) as pool:
        return pool.apply_async(func, args=args, kwds=kwds, **kwargs)
