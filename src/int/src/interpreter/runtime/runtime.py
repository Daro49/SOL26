"""
Single owner orchestrator of interpreter runtime

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from interpreter.input_model import Program
from interpreter.runtime.class_registry import ClassRegistry
from interpreter.runtime.bootstrap import Bootstrap
from interpreter.exec.execute import Execute
from interpreter.exec.dispatch import Dispatch
from typing import TextIO

class Runtime:
    """Interpreter runtime"""
    
    def __init__(self, program: Program, input_io: TextIO):
        self.registry = ClassRegistry()
        self.io = input_io
        self.bootstrapper = Bootstrap(self.registry)
        self.execute = Execute(self)
        self.dispatch = Dispatch(self.execute)