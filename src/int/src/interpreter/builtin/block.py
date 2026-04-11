"""
Built-in methods for Block class

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from interpreter.objectModel.sol_class import SolClass
from interpreter.objectModel.sol_object import SolObject
from interpreter.objectModel.sol_method import SolMethod
from interpreter.exec.context import Context
import interpreter.runtime.singletons as singletons

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from interpreter.runtime.runtime import Runtime

CLASS_NAME = "Block"

def register(_class: SolClass) -> None:
    """Register Block methods"""
    
    def _isBlock(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        """Block is Block"""
        
        return singletons.SOL_TRUE
    
    def _whileTrue(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        """while in SOL26"""
        
        result = singletons.SOL_NIL
    
        condition = _send_value(runtime, receiver)
        
        while condition.native_value == True:
            
            result = _send_value(runtime, args[0])
            
            condition = _send_value(runtime, receiver)
            
        return result
            
        
    def _send_value(
        runtime: Runtime,
        receiver: SolObject,
        ) -> SolObject:
        
        return runtime.dispatch.send(
            receiver=receiver,
            selector="value",
            args=[],
            context=Context(receiver),
            start_class=receiver.solclass
        )
        
    _class.methods.update({
        "isBlock":      SolMethod([], native_function=_isBlock),
        "whileTrue:":   SolMethod(["$a"], native_function=_whileTrue)
    })