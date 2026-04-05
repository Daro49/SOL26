"""
Class for representing a SOL26 object at the runtime
    Everything is an object

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from interpreter.objectModel.sol_class import SolClass

@dataclass
class SolObject:
    """
    Object representation at runtime
    Attributes: solclass:           class of the object instance
                instance_variables: optional object attributes
                native_value:       e.g. Integer has 10, String has "Hello"
    """

    solclass: SolClass
    instance_variables: dict[str, SolObject] = field(default_factory=dict)
    native_value: Any = None


    def get_instance_var(self, name: str) -> SolObject:
        """
        Get instance variable by name

        Args:
            name: of the instance variable

        Returns:
            SolObject
        """

        if name not in self.instance_variables:
            from ..error_codes import ErrorCode
            from ..exceptions import InterpreterError

            raise InterpreterError(ErrorCode(51), f"Undefined instance attribute: '{name}'")

        return self.instance_variables[name]


    def set_instance_var(self, name: str, value: SolObject) -> None:
        """
        Set new instance variable or sets value of existing one

        Args:
            name:   of the instance variable
            value:  to set

        Returns:
            None
        """
        self.instance_variables[name] = value
