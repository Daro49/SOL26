"""
Built-in methods for Nil class

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

CLASS_NAME = "Nil"

def register(_class: SolClass) -> None:
    """Register Nil methods"""

    _class.methods.update({
        "asString": SolMethod([], native_function=_asstring),
        "isNil":    SolMethod([], native_function=_isnil),
        "new":      SolMethod([], native_function=_new),
        "from:":    SolMethod(["$a"], native_function=_new)
    })

def _asstring(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """nil"""

    return SolObject(solclass=runtime.get_class("String"), native_value="nil")

def _isnil(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """true"""

    return singletons.SOL_TRUE
