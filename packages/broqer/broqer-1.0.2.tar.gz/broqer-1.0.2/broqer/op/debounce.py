"""
Emit a value only after a given idle time (emits meanwhile are skipped).
Debounce can also be used for a timeout functionality.

Usage:

>>> import asyncio
>>> from broqer import Subject, op
>>> s = Subject()
>>> _d = s | op.Debounce(0.1) | op.Sink(print)
>>> s.emit(1)
>>> s.emit(2)
>>> asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.05))
>>> s.emit(3)
>>> asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.15))
3
>>> _d.dispose()

When debounce is retriggered you can specify a value to emit:

>>> debounce_publisher = s | op.Debounce(0.1, False)
>>> _d = debounce_publisher | op.Sink(print)
>>> s.emit(False)
False
>>> asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.15))
>>> s.emit(True)
>>> asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.05))
>>> s.emit(False)
>>> asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.05))
>>> s.emit(True)
>>> asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.15))
True

Reseting is also possible:

>>> s.emit(False)
False
>>> s.emit(True)
>>> asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.15))
True
>>> debounce_publisher.reset()
False
>>> asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.15))

>>> _d.dispose()
"""
import asyncio
import sys
from typing import Any  # noqa

from broqer import Publisher, Subscriber, default_error_handler, NONE

from .operator import Operator


class Debounce(Operator):
    """ Emit a value only after a given idle time (emits meanwhile are
    skipped). Debounce can also be used for a timeout functionality.

    :param duetime: time in seconds to be waited for debounce
    :param retrigger_value: value used to emit when value has changed
    :param error_callback: error callback to be registered
    :param loop: asyncio loop to be used
    """
    def __init__(self, duetime: float,
                 retrigger_value: Any = NONE,
                 error_callback=default_error_handler, *, loop=None) -> None:

        if duetime < 0:
            raise ValueError('duetime has to be positive')

        Operator.__init__(self)

        self.duetime = duetime
        self._retrigger_value = retrigger_value
        self._call_later_handler = None  # type: asyncio.Handle
        self._error_callback = error_callback
        self._state = NONE  # type: Any
        self._next_state = NONE  # type: Any
        self._loop = loop or asyncio.get_event_loop()

    def unsubscribe(self, subscriber: Subscriber) -> None:
        Operator.unsubscribe(self, subscriber)
        if not self._subscriptions:
            self._state = NONE
            self._next_state = NONE
            if self._call_later_handler:
                self._call_later_handler.cancel()
                self._call_later_handler = None

    def get(self):
        if self._retrigger_value is not NONE and (
                not self._subscriptions or self._state is NONE):
            return self._retrigger_value
        return self._state

    def emit_op(self, value: Any, who: Publisher) -> None:
        if who is not self._publisher:
            raise ValueError('Emit from non assigned publisher')

        if value == self._next_state:
            # skip if emit will result in the same value as the scheduled one
            return

        if self._call_later_handler:
            self._call_later_handler.cancel()
            self._call_later_handler = None

        if self._retrigger_value is not NONE and \
           self._state != self._retrigger_value:
            # when retrigger_value is defined and current state is different
            self.notify(self._retrigger_value)
            self._state = self._retrigger_value
            self._next_state = self._retrigger_value
            if value == self._retrigger_value:
                # skip if emit will result in the same value as the current one
                return

        if value == self._state:
            self._next_state = self._state
            return

        self._next_state = value

        self._call_later_handler = \
            self._loop.call_later(self.duetime, self._debounced)

    def _debounced(self):
        self._call_later_handler = None
        try:
            self.notify(self._next_state)
            self._state = self._next_state
        except Exception:  # pylint: disable=broad-except
            self._error_callback(*sys.exc_info())

    def reset(self):
        """ Reset the debounce time """
        if self._retrigger_value is not NONE:
            self.notify(self._retrigger_value)
            self._state = self._retrigger_value
            self._next_state = self._retrigger_value
        if self._call_later_handler:
            self._call_later_handler.cancel()
            self._call_later_handler = None
