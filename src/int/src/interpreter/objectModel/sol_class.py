"""
Class for representing a SOL26 class at the runtime

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from interpreter.objectModel.sol_method import SolMethod

@dataclass
class SolClass:
    """
    Class representation at runtime
    Attributes: name:       name of the class
                superclass: class from which the class is inheriting
                methods:    dictionary of known methods of class
                is_native:  is built-in or user-defined
    """

    name: str
    superclass: SolClass | None
    methods: dict[str, SolMethod] = field(default_factory=dict)
    is_native: bool = False


    def lookup_method(self, selector: str) -> SolMethod | None:
        """
        Finds method based on selector, walks through to root parent class

        Args:
            selector: of the method

        Returns:
            SolMethod or None
        """

        current: SolClass | None = self

        while current is not None:
            if selector in current.methods:
                return current.methods[selector]

            current = current.superclass
        return None
