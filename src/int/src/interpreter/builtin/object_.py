"""
Built-in methods for Object class

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from typing import TYPE_CHECKING

import interpreter.runtime.singletons as singletons
from interpreter.objectModel.sol_class import SolClass
from interpreter.objectModel.sol_method import SolMethod
from interpreter.objectModel.sol_object import SolObject

if TYPE_CHECKING:
    from interpreter.runtime.runtime import Runtime

CLASS_NAME = "Object"

def register(_class: SolClass) -> None:
    """Register Object methods"""

    _class.methods.update({
        "identicalTo:": SolMethod(["$a"], native_function=_identicalto),
        "equalTo:":     SolMethod(["$a"], native_function=_equalto),
        "asString":     SolMethod([],     native_function=_asstring),
    })

    type_checks = [
        "isNumber",
        "isString",
        "isBlock",
        "isNil",
        "isBoolean"
    ]

    for method_name in type_checks:
        _class.methods[method_name] = SolMethod([], native_function=_isclass)

def _identicalto(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """is"""

    if receiver is args[0]:
        return singletons.SOL_TRUE

    return singletons.SOL_FALSE

def _equalto(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """=="""

    rec_val = receiver.native_value
    arg_val = args[0].native_value

    if rec_val is not None and arg_val is not None:
        if rec_val == arg_val:
            return singletons.SOL_TRUE

        return singletons.SOL_FALSE

    return _identicalto(runtime, receiver, args)

def _asstring(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """Object has no internal value"""

    return SolObject(solclass=runtime.get_class("String"), native_value="")

def _isclass(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """is specific class"""

    return singletons.SOL_FALSE
