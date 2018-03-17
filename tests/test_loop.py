#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import asyncio
from cl import Loop

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


async def wait_for_it(timeout):
    await asyncio.sleep(timeout)
    return 'success with timeout {}'.format(timeout)


class TestLoop(unittest.TestCase):
    def tearDown(self):
        asyncio.get_event_loop().stop()

    def test_get_event_loop(self):
        loop = Loop.get_event_loop()
        self.assertIsInstance(loop, asyncio.AbstractEventLoop)

    def test_get_existing_event_loop(self):
        existing_loop = asyncio.get_event_loop()
        loop = Loop.get_event_loop(existing_loop)

        self.assertIs(loop, existing_loop)

    def test_gather_futures(self):
        loop = Loop()
        self.assertIsNone(loop.futures)

        loop.gather(wait_for_it(0.1), wait_for_it(0.1))
        self.assertIsInstance(loop.futures, asyncio.Future)

    def test_gather_single_future(self):
        loop = Loop()
        self.assertIsNone(loop.futures)

        loop.gather(wait_for_it(0.1))
        self.assertIsInstance(loop.futures, asyncio.Task)
