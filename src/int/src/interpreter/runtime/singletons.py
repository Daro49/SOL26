"""
Representation of singletons during runtime
All in one separate file, so imports are easier and non duplicate

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from ..objectModel.sol_object import SolObject
from typing import cast, Any

SOL_NIL: SolObject = cast(Any, None)
SOL_TRUE: SolObject = cast(Any, None)
SOL_FALSE: SolObject = cast(Any, None)
