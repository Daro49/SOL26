"""
Class for representing a SOL26 class method at the runtime

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from __future__ import annotations

from collections.abc import Callable
from interpreter.objectModel.sol_object import SolObject
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, Callable

if TYPE_CHECKING:
    from interpreter.input_model import Method
    from interpreter.runtime.runtime import Runtime

class NativeCallable(Protocol):
    """Protocol for every native function"""
    
    def __call__(self, runtime: Runtime, receiver: SolObject, args: list[SolObject]) -> "SolObject": ...

@dataclass
class SolMethod:
    """
    Method representation at runtime
    Attributes: params:             method parameters
                body:               body if method is defined by user
                native_function:    if method is a native built-in function
    """

    params: list[str]
    body: Method | None = None
    native_function: NativeCallable | None = None

    @property
    def is_native(self) -> bool:
        """
        Get, Set boolean whether function is user-defined or built-in
        """

        return self.native_function is not None
