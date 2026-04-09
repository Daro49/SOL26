"""
React to messages (sends) and finds the right method to call execute

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from interpreter.exec.execute import Execute
from interpreter.objectModel.sol_object import SolObject
from interpreter.objectModel.sol_class import SolClass
from interpreter.exec.context import Context
from interpreter.exceptions import InterpreterError, ErrorCode

class Dispatch:
    """
    Message dispatcher, needs execute reference
    """ 
    
    def __init__(self, execute: Execute):
        """Setting execute reference"""
        self.execute = execute
        
    def send(
        self,
        receiver: SolObject,
        selector: str,
        args: list[SolObject],
        context: Context,
        start_class: SolClass | None = None
        ) -> SolObject:
        
        """
        Takes selector and receiver, finds appropriate method/attr

        Args:   receiver:       object of the message
                selector:       method selector
                args:           optional method arguments
                context:        execute context
                start_class:    where to start the lookup
   
        Returns: result of the method/attr
        """
        
        # Beware if not None
        method = start_class.lookup_method(selector)
        
        if method is None:
            return self._dnu(receiver, selector, args, start_class)
        
        if method.is_native:
            return method.native_function(self.execute.runtime, receiver, args)
        
        return self.execute.execute_method(
            method,
            receiver,
            selector,
            args,
            context
        )

    def _dnu(
        self,
        receiver: SolObject,
        selector: str,
        args: list[SolObject],
        start_class: SolClass | None
        ) -> SolObject:
        
        """Does not understand handler"""
        
        if len(args) == 0:
            if selector in receiver.instance_variables:
                return receiver.get_instance_var(selector)
            
            raise InterpreterError(
                ErrorCode(51),
                f"'{selector}' not found in instance of: "
                f"{receiver.solclass.name}"
            )
            
        elif len(args) == 1:
            method = start_class.lookup_method(selector[:-1])
            
            if method is None:
                receiver.set_instance_var(selector[:-1], args[0])
                return receiver
            
            raise InterpreterError(
                ErrorCode(54),
                f"Attribute collision with method: {selector}"
            )
        
        raise InterpreterError(
            ErrorCode(51),
            f"Does not understand: method '{selector}' not found"
        )
