"""
Class responsible for registering built-in classes

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

import interpreter.runtime.singletons as singletons
from interpreter.builtin import block, false, integer, nil, object_, string, true
from interpreter.error_codes import ErrorCode
from interpreter.exceptions import InterpreterError
from interpreter.input_model import Program
from interpreter.objectModel.sol_class import InternalAttribute, SolClass
from interpreter.objectModel.sol_object import SolObject
from interpreter.runtime.class_load import ClassLoad
from interpreter.runtime.class_registry import ClassRegistry

BUILTINS = [object_, nil, integer, string, true, false, block]


class Bootstrap:
    """Orchestrates the registration and linking of all built-in types."""

    def __init__(self, registry: ClassRegistry):
        """Store reference for registry"""
        self.registry = registry
        self.class_load = ClassLoad(registry)

    def bootstrap(self, program: Program) -> None:
        """Main method"""

        self._static_check(program)

        classes = self._make_builtin_classes()

        singletons.SOL_NIL = SolObject(solclass=classes["Nil"])
        singletons.SOL_TRUE = SolObject(solclass=classes["True"], native_value=True)
        singletons.SOL_FALSE = SolObject(solclass=classes["False"], native_value=False)

        self.registry.register_dict(classes)

        self._register_methods(classes)

        self.class_load.load(program)


    def _make_builtin_classes(self) -> dict[str, SolClass]:
        """
        Creates built-in classes

        !!! New classes should be added here !!!

        Returns:
            dict[str, SolClass]: built-in classes keyed by name
        """

        object_c = SolClass(name="Object", superclass=None, is_native=True)

        class_list = [
            object_c,
            SolClass(name="Nil", superclass=object_c, is_native=True),
            SolClass(name="True", superclass=object_c, is_native=True),
            SolClass(name="False", superclass=object_c, is_native=True),

            SolClass(
                name="Integer",
                superclass=object_c,
                is_native=True,
                internal_attr=InternalAttribute.INTEGER
            ),

            SolClass(
                name="String",
                superclass=object_c,
                is_native=True,
                internal_attr=InternalAttribute.STRING
            ),
            SolClass(
                name="Block",
                superclass=object_c,
                is_native=True,
                internal_attr=InternalAttribute.BLOCK
            )
        ]

        return {c.name: c for c in class_list}

    def _register_methods(self, classes: dict[str, SolClass]) -> None:
        """Registers built-in methods to it's classes"""

        for module in BUILTINS:
            name = getattr(module, "CLASS_NAME", None)

            if name and name in classes:
                module.register(classes[name])

        for _class in classes.values():
            for method in _class.methods.values():
                method.defined_on = _class

    def _static_check(self, program: Program) -> None:
        """Additional static checks that are not checked elsewhere"""

        for _class in program.classes:
            for method in _class.methods:
                arity = method.selector.count(":")

                if arity != method.block.arity:
                    raise InterpreterError(
                        ErrorCode(33),
                        f"Method: '{method}' arity "
                        f"doesn't match it's block arity!"
                    )
