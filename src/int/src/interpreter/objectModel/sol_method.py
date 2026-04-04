from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from interpreter.input_model import Method

@dataclass
class SolMethod:
    selector: str
    params: list[str]
    body: Method | None = None
    native_function: Callable | None = None
    
    @property
    def is_native(self) -> bool:
        return self.native_function is not None