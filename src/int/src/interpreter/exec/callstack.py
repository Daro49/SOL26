"""
Execution stack

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
        self._frames = list[Frames] = {}

    def push(self, receiver: str, selector: str) -> None:
        """Add frame on top"""
        self._frames.append(Frame(receiver, selector))
        
    def pop() -> None:
        """Delete frame on top"""
        self._frames.pop()
        