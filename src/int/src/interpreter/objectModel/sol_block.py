"""
Class for representing a SOL26 block at the runtime
    Block needs it model because it can be executed anytime, but not at definition

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from interpreter.exec.context import Context

    from ..input_model import Assign

@dataclass
class SolBlock:
    """
    Block representation at runtime
    Attributes: parameters: [ this part | ]
                assign:     [ | this part ]
                defining_context: needs the context the block was defined in
    """
    parameters: list[str]
    assigns: list[Assign]
    defining_context: Context
