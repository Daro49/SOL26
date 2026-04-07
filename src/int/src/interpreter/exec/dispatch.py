
from interpreter.exec.execute import Execute
from interpreter.objectModel.sol_object import SolObject

class Dispatch:
    def __init__(self, execute: Execute):
        self.execute = execute
        
    def send(self, ) -> SolObject: