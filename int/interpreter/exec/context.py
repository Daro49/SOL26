"""
Tracking context between calls

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from interpreter.error_codes import ErrorCode
from interpreter.exceptions import InterpreterError

if TYPE_CHECKING:
    from interpreter.objectModel.sol_object import SolObject

@dataclass
class Context:
    """
    Execution Context

    Attributes: self_object:    in which object's context
                outer:          parent object (caller)
                _locals:        local objects/variables
    """

    self_object: SolObject
    outer: Context | None = None
    _locals: dict[str, SolObject] = field(default_factory=dict, repr=False)

    def read(self, name: str) -> SolObject:
        """Returns object in local context by name"""

        context: Context | None = self

        while context is not None:
            if name in context._locals:
                return context._locals[name]

            context = context.outer

        raise InterpreterError(
            ErrorCode(32),
            f"Use of undefined variable: '{name}'!"
        )

    def write(self, name: str, value: SolObject) -> None:
        """Saves object to local context"""

        self._locals[name] = value

    def child(self, self_object: SolObject) -> Context:
        """Creates nested context, for blocks and calls"""

        return Context(
            self_object=self_object,
            outer=self
        )
