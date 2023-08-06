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


def getIterableLenForPbar(iterable, pbar=None, total=None):
    if pbar and total is  None:
        iterable = list(iterable)
        total = len(iterable)
    return iterable, total


def map(func, iterable, chunksize=None, workers=None, pbar=None, thread=False, total=None):
    mapFunc = "imap" if not thread else "map"
    chunksize = (chunksize or 1) if mapFunc == "imap" else chunksize
    items, total = getIterableLenForPbar(iterable, pbar=pbar, total=total)
    pbarConfig = parsePbarConfig(pbar)
    pbarConfig.update(total=total)
    poolClass = multiThread if thread else multiProcess
    with poolClass(workers) as pool:
        if mapFunc == "imap":
            with tqdm.tqdm(
                pool.imap(func, items, chunksize=chunksize), **pbarConfig
            ) as _pbar:
                results = list(_pbar)
        else:
            with tqdm.tqdm(**pbarConfig) as _pbar:
                runner = pbarRunner(_pbar)(func)
                results = pool.map(runner, items, chunksize=chunksize)
    return results


def imap(func, iterable, chunksize=1, workers=None, pbar=None, thread=False, total=None):
    items, total = getIterableLenForPbar(iterable, pbar=pbar, total=total)
    pbarConfig = parsePbarConfig(pbar)
    pbarConfig.update(total=total)
    poolClass = multiThread if thread else multiProcess
    with poolClass(workers) as pool:
        with tqdm.tqdm(
            pool.imap(func, items, chunksize=chunksize), **pbarConfig
        ) as _pbar:
            return _pbar


def starmap(func, iterable, chunksize=1, workers=None, pbar=None, thread=False, total=None):
    if pbar and not thread:
        raise Exception("Pbar is disabled when thread is False")
    items = list(iterable)
    poolClass = multiThread if thread else multiProcess
    if pbar:
        items, total = getIterableLenForPbar(iterable, pbar=pbar, total=total)
        pbarConfig = parsePbarConfig(pbar)
        pbarConfig.update(total=total)
        with poolClass(workers) as pool:
            with tqdm.tqdm(**pbarConfig) as _pbar:
                runner = pbarRunner(_pbar)(func)
                results = pool.starmap(runner, items, chunksize=chunksize)
    else:
        with poolClass(workers) as pool:
            results = pool.starmap(func, items, chunksize=chunksize)
    return results


def run(func, args=(), kwds=None, thread=False, **kwargs):
    poolClass = multiThread if thread else multiProcess
    with poolClass(1) as pool:
        return pool.apply_async(func, args=args, kwds=kwds, **kwargs)
