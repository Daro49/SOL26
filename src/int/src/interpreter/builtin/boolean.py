from interpreter.objectModel.sol_class import SolClass
from interpreter.objectModel.sol_object import SolObject
from interpreter.objectModel.sol_method import SolMethod
from interpreter.exec.dispatch import Dispatch
from interpreter.exec.context import Context
import interpreter.runtime.singletons as singletons

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from interpreter.runtime.runtime import Runtime

CLASS_NAME = "True"

def register(_class: SolClass, _classes: dict[str, SolClass]) -> None:
    
    def _asString(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        
        value = "true"
        
        if receiver.solclass == "False":
            value = "false"
        
        return SolObject(
            solclass=runtime.registry.get("String"),
            native_value=value
        )
        
    def _not(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        
        if receiver.solclass == "False":
            return singletons.SOL_TRUE
        
        return singletons.SOL_FALSE
    
    def _and(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        
        if receiver.solclass == "False":
            return singletons.SOL_FALSE
        
        return _send_value(runtime, args[0])
        
    def _or(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        
        if receiver.solclass == "True":
            return singletons.SOL_TRUE
        
        return _send_value(runtime, args[0])
    
    def _trueFalse(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        
        if receiver.solclass == "True":
            return _send_value(runtime, args[0])
        
        return _send_value(runtime, args[1])
    
    def _isBoolean(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        
        return singletons.SOL_TRUE
        
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
        
    boolean_methods = {
        "asString":        SolMethod([], native_function=_asString),
        "not":             SolMethod([], native_function=_not),
        "and:":            SolMethod(["$a"], native_function=_and),
        "or:":             SolMethod(["$a"], native_function=_or),
        "ifTrue:ifFalse:": SolMethod(["$a", "$b"], native_function=_trueFalse),
        "isBoolean":       SolMethod([], native_function=_isBoolean)
    }

    _classes.get("True").methods.update(boolean_methods)
    _classes.get("False").methods.update(boolean_methods)
    
    
