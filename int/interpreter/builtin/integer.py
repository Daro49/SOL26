"""
Built-in methods for Integer class

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from collections.abc import Callable
from functools import wraps
from typing import TYPE_CHECKING

import interpreter.runtime.singletons as singletons
from interpreter.error_codes import ErrorCode
from interpreter.exceptions import InterpreterError
from interpreter.objectModel.sol_class import SolClass
from interpreter.objectModel.sol_method import NativeCallable, SolMethod
from interpreter.objectModel.sol_object import SolObject

if TYPE_CHECKING:
    from interpreter.runtime.runtime import Runtime

CLASS_NAME = "Integer"

def register(_class: SolClass) -> None:
    """Register Integer methods"""

    _class.methods.update({
        "equalTo:":     SolMethod(["$a"], native_function=_equalto),
        "greaterThan:": SolMethod(["$a"], native_function=_greaterthan),
        "plus:":        SolMethod(["$a"], native_function=_plus),
        "minus:":       SolMethod(["$a"], native_function=_minus),
        "multiplyBy:":  SolMethod(["$a"], native_function=_multiplyby),
        "divBy:":       SolMethod(["$a"], native_function=_divby),
        "asString":     SolMethod([], native_function=_asstring),
        "asInteger":    SolMethod([], native_function=_asinteger),
        "isNumber":     SolMethod([], native_function=_isnumber),
        "timesRepeat:": SolMethod(["$a"], native_function=_timesrepeat),
        "new":          SolMethod([], native_function=_new)
    })

def int_op(
    func: Callable[[Runtime, int, int], SolObject]
    ) -> NativeCallable:
    """Handles unwrapping native_values and type checking for Integers."""

    @wraps(func)
    def wrapper(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        """Checks whether both object properties are numbers"""

        arg_val = args[0].native_value
        if not isinstance(arg_val, int):
            raise InterpreterError(
                ErrorCode(53),
                f"Bad argument type: {arg_val}!"
            )

        return func(runtime, receiver.native_value, arg_val)
    return wrapper

@int_op
def _equalto(
    runtime: Runtime,
    left: int,
    right: int
    ) -> SolObject:
    """=="""

    if left == right:
        return singletons.SOL_TRUE

    return singletons.SOL_FALSE

@int_op
def _greaterthan(
    runtime: Runtime,
    left: int,
    right: int
    ) -> SolObject:
    """>"""

    return singletons.SOL_TRUE if left > right else singletons.SOL_FALSE

@int_op
def _plus(
    runtime: Runtime,
    left: int,
    right: int
    ) -> SolObject:
    """+"""

    return SolObject(runtime.get_class("Integer"), native_value=left + right)

@int_op
def _minus(
    runtime: Runtime,
    left: int,
    right: int
    ) -> SolObject:
    """-"""

    return SolObject(runtime.get_class("Integer"), native_value=left - right)

@int_op
def _multiplyby(
    runtime: Runtime,
    left: int,
    right: int
    ) -> SolObject:
    """*"""

    return SolObject(runtime.get_class("Integer"), native_value=left * right)

@int_op
def _divby(
    runtime: Runtime,
    left: int,
    right: int
    ) -> SolObject:
    """//"""

    if right == 0:
        raise InterpreterError(ErrorCode(53), "Division by zero")

    return SolObject(runtime.get_class("Integer"), native_value=left // right)

def _asstring(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """str(int)"""

    return SolObject(
        runtime.get_class("String"),
        native_value=str(receiver.native_value)
    )

def _asinteger(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """self"""

    return receiver

def _isnumber(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """Integer is number"""

    return singletons.SOL_TRUE


def _timesrepeat(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """For loop in SOL26"""

    repeat = receiver.native_value

    result = singletons.SOL_NIL

    for i in range(1, repeat + 1):

        arg = SolObject(
            solclass=runtime.get_class("Integer"),
            native_value=i
        )

        result = runtime.dispatch.send(
            receiver=args[0],
            selector="value:",
            args=[arg],
            context=args[0].native_value.defining_context,
            start_class=args[0].solclass
        )

    return result

def _new(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    "Constructor new"

    receiver.native_value = 0
    return receiver
