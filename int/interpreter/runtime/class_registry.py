"""
Registry of all available classes for interpreter

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from interpreter.objectModel.sol_class import SolClass


class ClassRegistry:
    """Registers classes to it's attribute"""

    def __init__(self) -> None:
        """Instance attribute, dictionary of classes"""
        self._classes: dict[str, SolClass] = {}

    def register(self, sclass: SolClass) -> None:
        """Add class to registry"""
        self._classes[sclass.name] = sclass

    def register_dict(self, sclasses: dict[str, SolClass]) -> None:
        """Add dictionary of classes to registry"""
        self._classes.update(sclasses)

    def get(self, name: str) -> SolClass:
        """Retrieve class"""
        try:
            return self._classes[name]
        except KeyError:
            from interpreter.error_codes import ErrorCode
            from interpreter.exceptions import InterpreterError
            raise InterpreterError(
                ErrorCode(32),
                f"Unknown class: {name}"
            ) from None

    def has(self, name: str) -> bool:
        """Existence check"""
        return name in self._classes
