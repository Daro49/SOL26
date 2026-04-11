"""
Built-in methods for Integer class

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from interpreter.objectModel.sol_class import SolClass
from interpreter.objectModel.sol_object import SolObject
from interpreter.objectModel.sol_method import SolMethod, NativeCallable
from interpreter.exec.context import Context
from interpreter.exceptions import InterpreterError
from interpreter.error_codes import ErrorCode
import interpreter.runtime.singletons as singletons
from functools import wraps
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from interpreter.runtime.runtime import Runtime

CLASS_NAME = "Integer"

def register(_class: SolClass) -> None:
    """Register Integer methods"""
    
    def int_op(
        func: Callable[[Runtime, int, int], SolObject]
        ) -> NativeCallable:
        """Handles unwrapping native_values and type checking for Integers."""
        
        @wraps(func)
        def wrapper(
            runtime: Runtime,
            receiver: SolObject,
            args: list[SolObject]
            ) -> SolObject:
            """Checks whether both object properties are numbers"""
            
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
        """ == """
        
        if left == right:
            return singletons.SOL_TRUE
            
        return singletons.SOL_FALSE

    @int_op
    def _greaterThan(
        runtime: Runtime,
        left: int,
        right: int
        ) -> SolObject:
        """ > """
        
        return singletons.SOL_TRUE if left > right else singletons.SOL_FALSE

    @int_op
    def _plus(
        runtime: Runtime,
        left: int,
        right: int
        ) -> SolObject:
        """ + """
        
        return SolObject(runtime.get_class("Integer"), native_value=left + right)
    
    @int_op
    def _minus(
        runtime: Runtime,
        left: int,
        right: int
        ) -> SolObject:
        """ - """
        
        return SolObject(runtime.get_class("Integer"), native_value=left - right)
    
    @int_op
    def _multiplyBy(
        runtime: Runtime,
        left: int,
        right: int
        ) -> SolObject:
        """ * """
        
        return SolObject(runtime.get_class("Integer"), native_value=left * right)
    
    @int_op
    def _divBy(
        runtime: Runtime,
        left: int,
        right: int
        ) -> SolObject:
        """ // """
        
        if right == 0:
            raise InterpreterError(ErrorCode(53), "Division by zero")
        
        return SolObject(runtime.get_class("Integer"), native_value=left // right)
    
    def _asString(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        """str(int)"""
        
        return SolObject(
            runtime.get_class("String"),
            native_value=str(receiver.native_value)
        )
        
    def _asInteger(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        """self"""
        
        return receiver
        
    def _isNumber(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        """Integer is number"""
        
        return singletons.SOL_TRUE

    
    def _timesRepeat(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        """For loop in SOL26"""
        
        repeat = receiver.native_value
        
        result = singletons.SOL_NIL
        
        for i in range(1, repeat + 1):
            
            arg = SolObject(
                solclass=runtime.get_class("Integer"),
                native_value=i
            )
            
            result = runtime.dispatch.send(
                receiver=args[0],
                selector="value:",
                args=[arg],
                context=Context(args[0]),
                start_class=args[0].solclass
            )
            
        return result
    
    _class.methods.update({
        "equalTo:":     SolMethod(["$a"], native_function=_equalTo),
        "greaterThan:": SolMethod(["$a"], native_function=_greaterThan),
        "plus:":        SolMethod(["$a"], native_function=_plus),
        "minus:":       SolMethod(["$a"], native_function=_minus),
        "multiplyBy:":  SolMethod(["$a"], native_function=_multiplyBy),
        "divBy:":       SolMethod(["$a"], native_function=_divBy),
        "asString":     SolMethod([], native_function=_asString),
        "asInteger":    SolMethod([], native_function=_asInteger),
        "isNumber":     SolMethod([], native_function=_isNumber),
        "timesRepeat:": SolMethod(["$a"], native_function=_timesRepeat)
    })
        