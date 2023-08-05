"""
Emit the last received value periodically

Usage:

>>> import asyncio
>>> from broqer import Subject, op
>>> s = Subject()

>>> sample_publisher = s | op.Sample(0.015)

>>> _d = sample_publisher | op.Sink(print, 'Sample:')

>>> s.emit(1)
Sample: 1
>>> asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.06))
Sample: 1
...
Sample: 1

>>> s.emit((2, 3))
>>> asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.06))
Sample: (2, 3)
...
Sample: (2, 3)

>>> _d2 = sample_publisher | op.Sink(print, 'Sample 2:')
Sample 2: (2, 3)
>>> _d.dispose()
>>> asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.06))
Sample 2: (2, 3)
...
Sample 2: (2, 3)

>>> len(s.subscriptions) # how many subscriber are registered
1
>>> _d2.dispose()
>>> len(s.subscriptions)
0
>>> asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.02))
"""
import asyncio
import sys
from typing import Any  # noqa: F401

from broqer import Publisher, Subscriber, \
                   default_error_handler, NONE

from .operator import Operator


class Sample(Operator):
    """ Emit the last received value periodically

    :param interval: time in seconds between emits
    :param error_callback: the error callback to be registered
    :param loop: asyncio loop to use
    """
    def __init__(self, interval: float,
                 error_callback=default_error_handler, loop=None) -> None:
        if interval <= 0:
            raise ValueError('Interval has to be bigger than zero.')

        Operator.__init__(self)

        self._interval = interval
        self._call_later_handle = None
        self._loop = loop or asyncio.get_event_loop()
        self._state = NONE  # type: Any
        self._error_callback = error_callback

    def unsubscribe(self, subscriber: Subscriber) -> None:
        Operator.unsubscribe(self, subscriber)
        if not self._subscriptions:
            self._state = NONE

    def get(self):
        if not self._subscriptions:
            return self._publisher.get()  # may raises ValueError
        if self._state is not NONE:
            return self._state
        return Publisher.get(self)  # raises ValueError

    def _periodic_callback(self):
        """ Will be started on first emit """
        try:
            self.notify(self._state)  # emit to all subscribers
        except Exception:  # pylint: disable=broad-except
            self._error_callback(*sys.exc_info())

        if self._subscriptions:
            # if there are still subscriptions register next _periodic callback
            self._call_later_handle = \
                self._loop.call_later(self._interval, self._periodic_callback)
        else:
            self._state = NONE
            self._call_later_handle = None

    def emit_op(self, value: Any, who: Publisher) -> None:
        if who is not self._publisher:
            raise ValueError('Emit from non assigned publisher')

        self._state = value

        if self._call_later_handle is None:
            self._periodic_callback()
