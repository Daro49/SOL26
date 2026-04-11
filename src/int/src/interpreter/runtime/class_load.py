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
            _class.superclass = self.registry.get(class_node.parent)


    def _methods(self, program: Program) -> None:
        """Register classes' methods"""

        for class_node in program.classes:

            _class = self.registry.get(class_node.name)

            for method_node in class_node.methods:

                method = SolMethod(
                    params=[p.name for p in method_node.block.parameters],
                    body=method_node,
                    native_function=None
                )

                _class.methods[method_node.selector] = method
