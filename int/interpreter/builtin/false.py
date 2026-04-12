"""
Built-in methods for False class

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from typing import TYPE_CHECKING

import interpreter.runtime.singletons as singletons
from interpreter.builtin.object_ import _new
from interpreter.objectModel.sol_class import SolClass
from interpreter.objectModel.sol_method import SolMethod
from interpreter.objectModel.sol_object import SolObject

if TYPE_CHECKING:
    from interpreter.runtime.runtime import Runtime

CLASS_NAME = "False"

def register(_class: SolClass) -> None:
    """Register False methods"""

    _class.methods.update({
        "asString":        SolMethod([], native_function=_asstring),
        "not":             SolMethod([], native_function=_not),
        "and:":            SolMethod(["$a"], native_function=_and),
        "or:":             SolMethod(["$a"], native_function=_or),
        "ifTrue:ifFalse:": SolMethod(["$a", "$b"], native_function=_truefalse),
        "isBoolean":       SolMethod([], native_function=_isboolean),
        "new":      SolMethod([], native_function=_new),
        "from:":    SolMethod(["$a"], native_function=_new)
    })

def _asstring(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """false"""

    return SolObject(
        solclass=runtime.registry.get("String"),
        native_value="false"
    )

def _not(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """negation"""

    return singletons.SOL_TRUE

def _and(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """&&"""

    return singletons.SOL_FALSE

def _or(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """||"""

    return runtime.sendvalue(args[0])

def _truefalse(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """if in SOL26"""

    return runtime.sendvalue(args[1])

def _isboolean(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """true"""

    return singletons.SOL_TRUE
