"""
Execution stack, used for debugging only
could be used for run in future

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from dataclasses import dataclass


@dataclass
class Frame:
    """Stack unit representation"""
    receiver: str
    selector: str

class CallStack:
    """Stack of calls consisting of Frames"""

    def __init__(self) -> None:
        """Instance frames list"""
        self._frames: list[Frame] = []

    def push(self, receiver: str, selector: str) -> None:
        """Add frame on top"""
        self._frames.append(Frame(receiver, selector))

    def pop(self) -> None:
        """Delete frame on top"""
        self._frames.pop()
