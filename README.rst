************
Context loop
************

:Info: Context loop.
:Author: Paweł Zadrożny @pawelzny <pawel.zny@gmail.com>


Features
========

* Work with sync and async frameworks
* Schedule tasks to existing loop or create new one
* No need to understand how async works
* No callbacks required
* Run async tasks whenever and wherever you want


Installation
============

.. code:: bash

    pip install context-loop


**Package**: https://pypi.org/project/context-loop/


Documentation
=============

Read full documentation at http://context-loop.readthedocs.io/en/stable/


Quick Example
=============

.. code:: python

    >>> async def coro():
    ...     return await something_from_future()
    ...
    >>> import cl.Loop
    >>> with cl.Loop(coro(), coro(), coro()) as loop:
    ...    result = loop.run_until_complete()
    ...
    >>> result
    ['success', 'success', 'success']
