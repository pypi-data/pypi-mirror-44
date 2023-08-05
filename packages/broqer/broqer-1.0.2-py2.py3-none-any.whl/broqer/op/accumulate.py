"""
>>> from broqer import Subject, op
>>> s = Subject()

>>> def moving_average(state, value):
...     state=state[1:]+[value]
...     return state, sum(state)/len(state)

>>> lowpass = s | op.Accumulate(moving_average, init=[0]*3)
>>> lowpass | op.Sink(print)
<...>
>>> s.emit(3)
1.0
>>> s.emit(3)
2.0
>>> s.emit(3)
3.0
>>> s.emit(3)
3.0
"""
import asyncio
from typing import Any, Callable, Tuple
from functools import wraps

from broqer import Publisher, Subscriber, NONE

from .operator import Operator


class Accumulate(Operator):
    """ On each emit of source publisher a function gets called with state and
    received value as arguments and this returns a new state and value to emit.

    :param function:
        Function taking two arguments: current state and new value. The return
        value is a tuple with (new state, result) where new state will be used
        for the next call and result will be emitted to subscribers.
    :param init: initialization for state
    """
    def __init__(self, function: Callable[[Any, Any], Tuple[Any, Any]],
                 init: Any) -> None:
        Operator.__init__(self)
        self._function = function
        self._state = init
        self._init = init
        self._result = NONE

    def unsubscribe(self, subscriber: Subscriber) -> None:
        Operator.unsubscribe(self, subscriber)
        if not self._subscriptions:
            self._state = self._init
            self._result = NONE

    def get(self) -> Any:
        if self._result is not NONE:
            return self._result
        value = self._publisher.get()  # may be raises ValueError
        return self._function(self._init, value)[1]

    def emit_op(self, value: Any, who: Publisher) -> asyncio.Future:
        if who is not self._publisher:
            raise ValueError('Emit from non assigned publisher')

        self._state, self._result = self._function(self._state, value)
        return self.notify(self._result)

    def reset(self, state: Any) -> None:
        """ Reseting (or setting) the internal state.

        :param state: new state to be set
        """
        self._state = state


def build_accumulate(function: Callable[[Any, Any], Tuple[Any, Any]] = None, *,
                     init: Any = NONE):
    """ Decorator to wrap a function to return an Accumulate operator.

    :param function: function to be wrapped
    :param init: optional initialization for state
    """
    _init = init

    def _build_accumulate(function: Callable[[Any, Any], Tuple[Any, Any]]):
        @wraps(function)
        def _wrapper(init=NONE) -> Accumulate:
            init = _init if init is NONE else init
            if init is NONE:
                raise TypeError('"init" argument has to be defined')
            return Accumulate(function, init=init)
        return _wrapper

    if function:
        return _build_accumulate(function)

    return _build_accumulate
