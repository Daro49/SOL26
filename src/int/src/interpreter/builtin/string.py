from interpreter.objectModel.sol_class import SolClass
from interpreter.objectModel.sol_object import SolObject
from interpreter.objectModel.sol_method import SolMethod
import interpreter.runtime.singletons as singletons

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from interpreter.runtime.runtime import Runtime

CLASS_NAME = "String"

def register(_class: SolClass, _classes: dict[str, SolClass]) -> None:
    
    def _read(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        
        #string = runtime.io.readline().strip()
        string = input().strip()
        
        return SolObject(
            solclass=runtime.registry.get("String"),
            native_value=string
        )
        
    def _print(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:

        #runtime.io.write(receiver.native_value)
        #runtime.io.flush()
        
        print(receiver.native_value)
        
        return receiver
    
    def _equalTo(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        
        if receiver.native_value == args[0].native_value:
            return singletons.SOL_TRUE
        
        return singletons.SOL_FALSE
    
    def _asString(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        
        return receiver
    
    def _asInteger(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        
        try:
            num = int(receiver.native_value)
            
            return SolObject(
                solclass=runtime.registry.get("Integer"),
                native_value=num
            )
            
        except ValueError:
            return singletons.SOL_NIL
        
    def _concatenateWith(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        
        if args[0].solclass.name == "String":
            return SolObject(
                solclass=runtime.registry.get("String"),
                native_value=receiver.native_value + args[0].native_value
            )
            
        return singletons.SOL_NIL
    
    def _startEnd(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        
        start = args[0].native_value
        end = args[1].native_value
        
        if (args[0].solclass != "Integer" or start < 0 
            or
           args[1].solclass != "Integer" or end < 0):
            
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
        
        return SolObject(
            solclass=runtime.registry.get("Integer"),
            native_value=len(receiver.native_value)
        )
        
    _class.methods.update({
        "read":             SolMethod([], native_function=_read),
        "print":            SolMethod([], native_function=_print),
        "equalTo:":         SolMethod(["$a"], native_function=_equalTo),
        "asString":         SolMethod([], native_function=_asString),
        "asInteger":        SolMethod([], native_function=_asInteger),
        "concatenateWith:":         SolMethod(
            ["$a"], native_function=_concatenateWith
        ),
        
        "startsWith:endsBefore:":   SolMethod(
            ["$a", "$b"], native_function=_startEnd
        ),
        
        "length":           SolMethod([], native_function=_length),
    })