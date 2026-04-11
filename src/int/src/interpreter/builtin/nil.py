"""
Built-in methods for Nil class

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from interpreter.objectModel.sol_class import SolClass
from interpreter.objectModel.sol_object import SolObject
from interpreter.objectModel.sol_method import SolMethod
import interpreter.runtime.singletons as singletons
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from interpreter.runtime.runtime import Runtime

CLASS_NAME = "Nil"

def register(_class: SolClass) -> None:
    """Register Nil methods"""
    
    def _asString(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        """nil"""
        
        return SolObject(solclass=runtime.get_class("String"), native_value="nil")

    def _isNil(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        """true"""
        
        return singletons.SOL_TRUE
    
    _class.methods.update({
        "asString": SolMethod([], native_function=_asString),
        "isNil":    SolMethod([], native_function=_isNil)
    })
