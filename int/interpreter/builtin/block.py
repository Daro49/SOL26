"""
Built-in methods for Block class

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from typing import TYPE_CHECKING

import interpreter.runtime.singletons as singletons
from interpreter.exec.context import Context
from interpreter.objectModel.sol_block import SolBlock
from interpreter.objectModel.sol_class import SolClass
from interpreter.objectModel.sol_method import SolMethod
from interpreter.objectModel.sol_object import SolObject

if TYPE_CHECKING:
    from interpreter.runtime.runtime import Runtime

CLASS_NAME = "Block"

def register(_class: SolClass) -> None:
    """Register Block methods"""

    _class.methods.update({
        "isBlock":      SolMethod([], native_function=_isblock),
        "whileTrue:":   SolMethod(["$a"], native_function=_whiletrue),
        "new":          SolMethod([], native_function=_new)
    })

def _isblock(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """Block is Block"""

    return singletons.SOL_TRUE

def _whiletrue(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    """while in SOL26"""

    result = singletons.SOL_NIL

    condition = runtime.sendvalue(receiver)

    while condition is singletons.SOL_TRUE:

        result = runtime.sendvalue(args[0])

        condition = runtime.sendvalue(receiver)

    return result

def _new(
    runtime: Runtime,
    receiver: SolObject,
    args: list[SolObject]
    ) -> SolObject:
    "Constructor new"

    block = SolBlock(
        parameters=[],
        assigns=[],
        defining_context=Context(receiver)
    )

    method = SolMethod(
        params=[],
        native_function=runtime.execute.execute_block
    )

    return SolObject(
        solclass=runtime.get_class("Block"),
        instance_methods={"value": method},
        native_value=block
    )
