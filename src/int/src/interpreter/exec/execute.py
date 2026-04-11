"""
Input node walkthrough and execution

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from interpreter.input_model import Expr, Assign, Var, Literal, Send, Block
from interpreter.exec.callstack import CallStack
from interpreter.objectModel.sol_method import SolMethod
from interpreter.objectModel.sol_object import SolObject
from interpreter.objectModel.sol_block import SolBlock
from interpreter.exec.context import Context
from interpreter.exceptions import InterpreterError
from interpreter.error_codes import ErrorCode

if TYPE_CHECKING:
    from interpreter.runtime.runtime import Runtime

from interpreter.runtime.singletons import SOL_NIL, SOL_TRUE, SOL_FALSE

class Execute:
    """Class that walks input model and executes"""
    
    def __init__(self, runtime: Runtime):
        """Needs reference to runtime (ClassRegistry) and own CallStack"""
        self.runtime = runtime
        self.call_stack = CallStack()
    
    def execute_method(
        self,
        method: SolMethod,
        receiver: SolObject,
        selector: str,
        args: list[SolObject],
        outer_context: Context | None = None
        ) -> SolObject:
        """
        Creates new context, iterates over every assignment

        Args:   method:         to execute
                receiver:       object receiving message
                args:           method arguments
                outer_context:  where the call is from

        Returns: result of the last assign as object
        """
        
        self.call_stack.push(receiver.solclass.name, selector)
        context = Context(self_object=receiver, outer=outer_context)
        
        # Optionally write arguments as locals in the new context
        for param, arg in zip(method.params, args):
            context.write(param, arg)
            
        try:
            result = SOL_NIL
            
            if method.body is None:
                raise InterpreterError(
                    ErrorCode(52),
                    "Method body not populated correctly"
                )
            
            for assign in method.body.block.assigns:
                result = self.visit_Assign(assign, context)
                
            return result
        finally:
            self.call_stack.pop()
    
    def execute_block(
        self,
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        """
        Similiar to method, but needs its defining context

        !!! used for reference blocks !!!

        Args:   block: model
                args: block arguments

        Returns: result of the last assign as object
        """
        
        block = receiver.native_value
        
        context = block.defining_context
        
        for param, arg in zip(block.parameters, args):
            context.write(param, arg)
            
        result = SOL_NIL
        
        for assign in block.assigns:
            result = self.visit_Assign(assign, context)
            
        return result
    
    def visit_Expr(self, node: Expr, context: Context) -> SolObject:
        """Expression crossroad"""
        
        if node.literal is not None:
            return self.visit_Literal(node.literal, context)
        
        if node.var is not None:
            return self.visit_Var(node.var, context)
        
        if node.block is not None:
            return self.visit_Block(node.block, context)
        
        if node.send is not None:
            return self.visit_Send(node.send, context)
        
        raise InterpreterError(
            ErrorCode(20),
            "Malformed XML"
        )
    
    def visit_Assign(self, node: Assign, context: Context) -> SolObject:
        """
        := operator
        
        Args:   node:       Assign from input model
                context:    to write vars in

        Returns: result in case it's the last assign of block
        """
        
        value = self.visit_Expr(node.expr, context)
        
        if node.target.name != '_':
            context.write(node.target.name, value)
            
        return value

    def visit_Var(self, node: Var, context: Context) -> SolObject:
        """Returns context variable or singleton"""
        match node.name:
            case "self":    return context.self_object
            case "super":   return context.self_object
            case "nil":     return SOL_NIL
            case "true":    return SOL_TRUE
            case "false":   return SOL_FALSE
            case _:         return context.read(node.name)
            
    def visit_Literal(self, node: Literal, context: Context) -> SolObject:
        """Creates object based on literal class"""
        
        match node.class_id:
            case "Integer":
                return SolObject(
                    solclass=self.runtime.registry.get("Integer"),
                    native_value=int(node.value)
                )
            
            case "String":
                return SolObject(
                    solclass=self.runtime.registry.get("String"),
                    native_value=node.value
                )
                
            case "Nil":
                return SOL_NIL
            case "True":
                return SOL_TRUE
            case "False":
                return SOL_FALSE
            
            case "class":
                return SolObject(
                    solclass=self.runtime.registry.get(node.value)
                )
            
            case _:
                raise InterpreterError(
                    ErrorCode(52), "How did you get here"
                )
        
    def visit_Send(self, node: Send, context: Context) -> SolObject:
        """Send node handler"""
        
        if node.selector == "new":
            return self.visit_Expr(node.receiver, context)
        
        # TODO from: message
        
        receiver = self.visit_Expr(node.receiver, context)
        args = [self.visit_Expr(arg.expr, context) for arg in node.args]
        lookup_class = receiver.solclass
        
        if (node.receiver.var is not None
            and node.receiver.var.name == "super" 
            and lookup_class.superclass is not None
        ):
            lookup_class = lookup_class.superclass
            
        return self.runtime.dispatch.send(
            receiver=receiver,
            selector=node.selector,
            args=args,
            context=context,
            start_class=lookup_class
        )
        
    
    def visit_Block(self, node: Block, context: Context) -> SolObject:
        """Wrapper into SolObject for later execution"""
       
        parameter_names = [p.name for p in node.parameters]
        
        # -^-^-^-^-^-^-^-^ BLOCK CHECKS -^-^-^-^-^-^-^-^ #
        
        if len(parameter_names) != len(set(parameter_names)):
            raise InterpreterError(
                ErrorCode(35),
                "Name collision of Block parameters!"
            )
        
        for assign in node.assigns:
            if assign.target.name in parameter_names:
                raise InterpreterError(
                    ErrorCode(34),
                    f"Assigning to a parameter: '{assign.target.name}' "
                    "in Block!"
                )
                
        # -^-^-^-^-^-^-^-^ BLOCK CHECKS -^-^-^-^-^-^-^-^ #
        
        sol_block = SolBlock(
            parameters=parameter_names,
            assigns=node.assigns,
            defining_context=context
        ) #Capturing context!
        
        block_method = SolMethod(
            params=[p.name for p in node.parameters],
            native_function=self.execute_block
        )
        
        selector = "value"
        
        if node.arity > 0:
            selector = "value:" * node.arity
        
        return SolObject(
            solclass=self.runtime.registry.get("Block"),
            instance_methods={selector: block_method},
            native_value=sol_block
        )