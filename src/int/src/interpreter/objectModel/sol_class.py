from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sol_method import SolMethod

@dataclass
class SolClass:
    name: str
    superclass: SolClass | None
    methods: dict[str, SolMethod] = field(default_factory=dict)
    is_native: bool = False
    
    def lookup_method(self, selector: str) -> SolMethod | None:
        current: SolClass | None = self
        
        while current is not None:
            if selector in current.methods:
                return current.methods[selector]
            
            current = current.superclass
        return None