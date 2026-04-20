"""
Loads user defined classes and method to object model

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

from interpreter.error_codes import ErrorCode
from interpreter.exceptions import InterpreterError
from interpreter.input_model import Program
from interpreter.objectModel.sol_class import SolClass
from interpreter.objectModel.sol_method import SolMethod
from interpreter.runtime.class_registry import ClassRegistry


class ClassLoad:
    """
    Class for loading user defined classes & methods into object model
    """

    def __init__(self, registry: ClassRegistry):
        """Needs class registry to register into"""
        self.registry = registry

    def load(self, program: Program) -> None:
        """
        Loads user program and it's classes & methods

        Args: program: structure from input model
        """

        self._classes(program)
        self._superclasses(program)
        self._methods(program)

    def _classes(self, program: Program) -> None:
        """Register classes"""

        for class_node in program.classes:

            if self.registry.has(class_node.name):
                raise InterpreterError(
                    ErrorCode(35),
                    f"Redefinition of class: {class_node.name}"
                )

            self.registry.register(
                SolClass(
                    name=class_node.name,
                    superclass=None,
                    is_native=False
                )
            )

        if not self.registry.has("Main"):
            raise InterpreterError(
                ErrorCode(31),
                "Missing class 'Main'!"
            )

    def _superclasses(self, program: Program) -> None:
        """Register classes' parents"""

        for class_node in program.classes:

            _class = self.registry.get(class_node.name)
            parent = self.registry.get(class_node.parent)

            _class.superclass = parent
            _class.internal_attr = parent.internal_attr

            self._check_circular_inheritance(program)


    def _methods(self, program: Program) -> None:
        """Register classes' methods"""

        for class_node in program.classes:

            _class = self.registry.get(class_node.name)

            for method_node in class_node.methods:

                if method_node.selector in _class.methods:
                    raise InterpreterError(
                        ErrorCode(35),
                        f"Redefinition of method: '{method_node.selector}' "
                        f"in class: '{_class.name}'!"
                    )

                method = SolMethod(
                    params=[p.name for p in method_node.block.parameters],
                    body=method_node,
                    native_function=None
                )

                _class.methods[method_node.selector] = method

    def _check_circular_inheritance(self, program: Program) -> None:
        """Detect circular inheritance chains"""

        for class_node in program.classes:
            self._detect_cycle(class_node.name, set())

    def _detect_cycle(self, class_name: str, visited: set[str]) -> None:
        """Follow the inheritance chain to detect cycles"""

        if class_name in visited:
            raise InterpreterError(
                ErrorCode(35),
                f"Circular inheritance detected involving class: {class_name}"
            )

        _class = self.registry.get(class_name)

        if _class.superclass is None:
            return

        visited.add(class_name)
        self._detect_cycle(_class.superclass.name, visited)
