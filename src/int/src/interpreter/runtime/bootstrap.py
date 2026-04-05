"""
Class responsible for registering built-in classes

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

import interpreter.runtime.singletons as singletons
from interpreter.objectModel.sol_class import SolClass
from interpreter.objectModel.sol_object import SolObject
from interpreter.runtime.class_registry import ClassRegistry


class Bootstrap:
    """Orchestrates the registration and linking of all built-in types."""

    def __init__(self, registry: ClassRegistry):
        """Store reference for registry"""
        self.registry = registry

    def bootstrap(self) -> None:
        """Main method"""
        classes = self._make_builtin_classes()

        singletons.SOL_NIL = SolObject(solclass=classes["Nil"])
        singletons.SOL_TRUE = SolObject(solclass=classes["True"], native_value=True)
        singletons.SOL_FALSE = SolObject(solclass=classes["False"], native_value=False)

        # TODO: Register built-in methods to built-in classes

        self.registry.register_dict(classes)


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
            SolClass(name="Integer", superclass=object_c, is_native=True),
            SolClass(name="String", superclass=object_c, is_native=True),
            SolClass(name="Block", superclass=object_c, is_native=True)
        ]

        return {c.name: c for c in class_list}
