from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sol_class import SolClass

@dataclass
class SolObject:
    solclass: SolClass
    instance_variables: dict[str, SolObject] = field(default_factory=dict)
    native_value: Any = None
    
    def get_instance_var(self, name: str) -> SolObject:
        
        if name not in self.instance_variables:
            from ..exceptions import InterpreterError
            
            raise InterpreterError(51, f"Undefined instance attribute: '{name}'")
        
        return self.instance_variables[name]

    def set_instance_var(self, name: str, value: SolObject) -> None:
        self.instance_variables[name] = value
