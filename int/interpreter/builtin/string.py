"""
Built-in methods for String class

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from typing import TYPE_CHECKING

import interpreter.runtime.singletons as singletons
from interpreter.objectModel.sol_class import SolClass
from interpreter.objectModel.sol_method import SolMethod
from interpreter.objectModel.sol_object import SolObject

if TYPE_CHECKING:
    from interpreter.runtime.runtime import Runtime

CLASS_NAME = "String"

def register(_class: SolClass) -> None:
    """Register String methods"""

    _class.methods.update({
        "read":             SolMethod([], native_function=_read),
        "print":            SolMethod([], native_function=_print),
        "equalTo:":         SolMethod(["$a"], native_function=_equalto),
        "asString":         SolMethod([], native_function=_asstring),
        "asInteger":        SolMethod([], native_function=_asinteger),
        "concatenateWith:":         SolMethod(
            ["$a"], native_function=_concatenatewith
        ),

        "startsWith:endsBefore:":   SolMethod(
            ["$a", "$b"], native_function=_startend
        ),

        "length":           SolMethod([], native_function=_length),
        "isString":         SolMethod([], native_function=_isstring),
        "new":              SolMethod([], native_function=_new)
    })

def _read(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """read from input"""

    string = runtime.io.readline().strip()

    return SolObject(
        solclass=runtime.registry.get("String"),
        native_value=string
    )

def _print(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """print to output"""

    #runtime.io.write(receiver.native_value)
    #runtime.io.flush()

    print(receiver.native_value)

    return receiver

def _equalto(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """=="""

    if receiver.native_value == args[0].native_value:
        return singletons.SOL_TRUE

    return singletons.SOL_FALSE

def _asstring(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """self"""

    return receiver

def _asinteger(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """int(str)"""

    try:
        num = int(receiver.native_value)

        return SolObject(
            solclass=runtime.registry.get("Integer"),
            native_value=num
        )

    except ValueError:
        return singletons.SOL_NIL

def _concatenatewith(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """+"""

    if args[0].solclass.name == "String":
        return SolObject(
            solclass=runtime.registry.get("String"),
            native_value=receiver.native_value + args[0].native_value
        )

    return singletons.SOL_NIL

def _startend(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """substring"""

    start = args[0].native_value
    end = args[1].native_value

    if (args[0].solclass.name != "Integer" or start < 0
        or
        args[1].solclass.name != "Integer" or end < 0):

        return singletons.SOL_NIL

    return SolObject(
        solclass=runtime.registry.get("String"),
        native_value=receiver.native_value[start:end]
    )

def _length(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """len()"""

    return SolObject(
        solclass=runtime.registry.get("Integer"),
        native_value=len(receiver.native_value)
    )

def _isstring(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """true"""

    return singletons.SOL_TRUE

def _new(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    "Constructor new"

    receiver.native_value = ""
    return receiver
