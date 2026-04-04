from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..input_model import Assign

@dataclass
class SolBlock:
    paramters: list[str]
    assign: list[Assign]
    defining_context: "ExecutionContext" # TODO