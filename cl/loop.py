#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from typing import Union

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


class Loop:
    """Asyncio Event loop context manager.

    Context manager which get existing event loop or if none exist
    will create new one.

    All coroutines are converted to task and scheduled to execute in near future.
    Scheduling is safe for long running tasks.

    :Example:

    Create coroutine using `@asyncio.coroutine` decorator or
    with async/await syntax

    .. code-block:: python

        >>> async def wait_for_it(timeout):
        ...    await asyncio.sleep(timeout)
        ...    return 'success sleep for {} seconds'.format(timeout)
        ...

    Use context manager to get result from one or more coroutines

    .. code-block:: python

        >>> with Loop(wait_for_it(5), wait_for_it(3), return_exceptions=True) as loop:
        ...    result = loop.run_until_complete()
        ...
        >>> result
        ['success sleep for 3 seconds', 'success sleep for 5 seconds']

    When single coroutine has been scheduled to run, only single value will
    be returned.

    .. code-block:: python

        >>> with Loop(wait_for_it(4)) as loop:
        ...    result = loop.run_until_complete()
        ...
        >>> result
        'success sleep for 4 seconds'


    :param futures: One or more coroutine or future.
    :type futures: asyncio.Future, asyncio.coroutine
    :param loop: Optional existing loop.
    :type loop: asyncio.AbstractEventLoop
    :param return_exceptions: If True will return exceptions as result.
    :type return_exceptions: Boolean
    :param stop_when_done: If True will close the loop on context exit.
    :type stop_when_done: Boolean
    """

    futures = None
    """Gathered futures."""

    def __init__(self, *futures, loop=None, return_exceptions=False):
        self.loop = self.get_event_loop(loop)
        self.return_exceptions = return_exceptions
        self.ft_count = 0
        if futures:
            self.gather(*futures)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.loop = None
        self.futures = None

    @staticmethod
    def get_event_loop(loop: asyncio.AbstractEventLoop = None) -> asyncio.AbstractEventLoop:
        """Get existing loop or create new one.

        :param loop: Optional, already existing loop.
        :type loop: asyncio.AbstractEventLoop
        :return: Asyncio loop
        :rtype: asyncio.AbstractEventLoop
        """
        if loop:
            return loop
        return asyncio.new_event_loop()

    def gather(self, *futures: Union[asyncio.Future, asyncio.coroutine]):
        """Gather list of futures/coros and return single Task ready to schedule.

        :Example:

        Prepare all futures to execution

        .. code-block:: python

            >>> async def do_something():
            ...    return 'something'
            ...
            >>> async def do_something_else():
            ...    return 'something_else'
            ...

        Gather all tasks and then pass to context loop

        .. code-block:: python

            >>> loop = Loop(return_exceptions=True)
            >>> loop.gather(do_something(), do_something_else())
            >>> with loop as l:
            ...    result = l.run_until_complete()
            ...
            >>> result
            ['something', 'something_else']


        :param futures: One or more coroutine or future.
        :type futures: asyncio.Future, asyncio.coroutine
        :return: Futures grouped into single future
        :rtype: asyncio.Task, asyncio.Future
        """
        self.ft_count = len(futures)
        self.futures = asyncio.gather(*futures, loop=self.loop,
                                      return_exceptions=self.return_exceptions)

    def run_until_complete(self):
        """Run loop until all futures are done.

        Order of result data will be the same as order of given coros.

        :return: Result, list of results or None if task has been cancelled.
        :rtype: None, list, Any
        """
        try:
            result = self.loop.run_until_complete(self.futures)
        except asyncio.futures.CancelledError:
            return None
        else:
            if self.ft_count == 1:
                return result[0]
            return result

    def cancel(self):
        """Cancel pending futures."""
        self.futures.cancel()
