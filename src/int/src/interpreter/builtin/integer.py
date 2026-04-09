from interpreter.objectModel.sol_class import SolClass
from interpreter.objectModel.sol_object import SolObject
from interpreter.objectModel.sol_method import SolMethod
from interpreter.exceptions import InterpreterError, ErrorCode
import interpreter.runtime.singletons as singletons
from functools import wraps
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from interpreter.runtime.runtime import Runtime

CLASS_NAME = "Integer"

def register(_class: SolClass, _classes: dict[str, SolClass]) -> None:
    
    def int_op(func):
        """Handles unwrapping native_values and type checking for Integers."""
        @wraps(func)
        def wrapper(
            runtime: Runtime,
            receiver: SolObject,
            args: list[SolObject]
            ) -> SolObject:
            
            arg_val = args[0].native_value
            if not isinstance(arg_val, int):
                return singletons.SOL_FALSE
            
            return func(runtime, receiver.native_value, arg_val)
        return wrapper
    
    @int_op
    def _equalTo(
        runtime: Runtime,
        left: int,
        right: int
        ) -> SolObject:
        
        if left == right:
            return singletons.SOL_TRUE
            
        return singletons.SOL_FALSE

    @int_op
    def _greaterThan(
        runtime: Runtime,
        left: int,
        right: int
        ) -> SolObject:
        
        return singletons.SOL_TRUE if left > right else singletons.SOL_FALSE

    @int_op
    def _plus(
        runtime: Runtime,
        left: int,
        right: int
        ) -> SolObject:
        
        return SolObject(_classes.get("Integer"), native_value=left + right)
    
    @int_op
    def _minus(
        runtime: Runtime,
        left: int,
        right: int
        ) -> SolObject:
        
        return SolObject(_classes.get("Integer"), native_value=left - right)
    
    @int_op
    def _multiplyBy(
        runtime: Runtime,
        left: int,
        right: int
        ) -> SolObject:
        
        return SolObject(_classes.get("Integer"), native_value=left * right)
    
    @int_op
    def _divBy(
        runtime: Runtime,
        left: int,
        right: int
        ) -> SolObject:
        
        if right == 0:
            raise InterpreterError(ErrorCode(53), "Division by zero")
        
        return SolObject(_classes.get("Integer"), native_value=left // right)
    
    def _asString(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        
        return SolObject(
            _classes.get("String"),
            native_value=str(receiver.native_value)
        )
        
    def _asInteger(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        
        return SolObject(
            _classes.get("Integer"),
            native_value=receiver.native_value
        )
        
    # TODO timesRepeat:
    
    _class.methods.update({
        "equalTo:":     SolMethod(["$a"], native_function=_equalTo),
        "greaterThan:": SolMethod(["$a"], native_function=_greaterThan),
        "plus:":        SolMethod(["$a"], native_function=_plus),
        "minus:":       SolMethod(["$a"], native_function=_minus),
        "multiplyBy:":  SolMethod(["$a"], native_function=_multiplyBy),
        "divBy:":       SolMethod(["$a"], native_function=_divBy),
        "asString":     SolMethod([], native_function=_asString),
        "asInteger":    SolMethod([], native_function=_asInteger)
    })
        