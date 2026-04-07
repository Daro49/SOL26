"""
Input node walkthrough and execution

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from interpreter.input_model import Method, Expr, Assign, Var

from interpreter.exec.callstack import CallStack
from interpreter.objectModel.sol_method import SolMethod
from interpreter.objectModel.sol_object import SolObject
from interpreter.objectModel.sol_block import SolBlock
from interpreter.exec.context import Context

from interpreter.runtime.singletons import SOL_NIL, SOL_TRUE, SOL_FALSE

class Execute:
    """
    Class that walks input model and executes
    """
    
    def __init__(self, runtime: Runtime):
        """Needs reference to runtime (ClassRegistry) and own CallStack"""
        self.runtime = runtime
        self.call_stack = CallStack()
    
    def execute_method(
        self,
        method: SolMethod,
        receiver: SolObject,
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
        
        self.call_stack.push(receiver.solclass.name, method.selector)
        context = Context(self_object=receiver, outer=outer_context)
        
        # Optionally write arguments as locals in the new context
        for param, arg in zip(method.params, args):
            context.write(param, arg)
            
        try:
            result = SOL_NIL
            
            for assign in method.body.block.assigns:
                result = self.visit_Assign(assign, context)
                
            return result
        finally:
            self.call_stack.pop()
    
    def execute_block(
        self,
        block: SolBlock,
        args: list[SolObject]
        ) -> SolObject:
        """
        Similiar to method, but needs its defining context

        !!! used for reference blocks !!!

        Args:   block: model
                args: block arguments

        Returns: result of the last assign as object
        """
        
        context = block.defining_context.child()
        
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
        match node.name:
            case "self":    return context.self_object
            case "super":   return context.self_object
            case "nil":     return SOL_NIL
            case "true":    return SOL_TRUE
            case "false":   return SOL_FALSE
            case _:         return context.read(node.name)