"""
Single owner orchestrator of interpreter runtime

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from interpreter.input_model import Program
from interpreter.runtime.class_registry import ClassRegistry
from interpreter.runtime.bootstrap import Bootstrap
from interpreter.exec.execute import Execute
from interpreter.exec.dispatch import Dispatch
from interpreter.objectModel.sol_object import SolObject
from interpreter.objectModel.sol_class import SolClass
from interpreter.exceptions import InterpreterError
from interpreter.error_codes import ErrorCode
from typing import TextIO

class Runtime:
    """Interpreter runtime"""
    
    def __init__(self, input_io: TextIO):
        """All runtime dependencies"""
        
        self.registry = ClassRegistry()
        self.io = input_io
        self.bootstrap = Bootstrap(self.registry)
        self.execute = Execute(self)
        self.dispatch = Dispatch(self.execute)
        
    def run_main(self, program: Program) -> None:
        """Starts execution of program"""
        
        self.bootstrap.bootstrap(program)
        
        main_class = self.registry.get("Main")
        main_instance = SolObject(solclass=main_class)
        run_method = main_class.lookup_method("run")
        
        if run_method is None:
            raise InterpreterError(
                ErrorCode(31),
                "Missing method 'run' in class 'Main'!"
            )
        
        self.execute.execute_method(run_method, main_instance, "run", args=[])
        
    def get_class(self, name: str) -> SolClass:
        """Python .get wrapper"""
        
        _class = self.registry.get(name)
        
        if _class is None:
            raise InterpreterError(
                ErrorCode(52),
                "Class registry did not populate correctly"
            )
            
        return _class