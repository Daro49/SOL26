"""
Test

Bootstrapper functionality test

Author: Matej Daranský <xdaranm00@stud.fit.vut.cz>
"""

import interpreter.runtime.singletons as singletons
from interpreter.runtime.bootstrap import Bootstrap
from interpreter.runtime.class_registry import ClassRegistry


def test_bootstrap_logic() -> None:
    print("Starting test for Bootstrapper...")

    # 1. SETUP
    registry = ClassRegistry()
    bootstrapper = Bootstrap(registry)

    # 2. EXECUTION
    bootstrapper.bootstrap()

    # 3. ASSERTIONS - Registry
    assert registry.has("Object"), "Registry should have object"
    assert registry.has("Nil"), "Registry should have Nil"
    assert registry.has("Integer"), "Registry should have Integer"

    # Inheritance check
    nil_class = registry.get("Nil")
    object_class = registry.get("Object")
    assert nil_class.superclass == object_class, "Nil should inherit from Object"

    # 4. ASSERTIONS - Singletons
    assert singletons.SOL_NIL is not None, "SOL_NIL should not be None"
    assert singletons.SOL_NIL.solclass.name == "Nil", "SOL_NIL should have class Nil"

    assert singletons.SOL_TRUE.native_value is True, "SOL_TRUE should have native_value True"
    assert singletons.SOL_TRUE.solclass.name == "True", "SOL_TRUE should have class True"

    assert singletons.SOL_FALSE.native_value is False, "SOL_FALSE should have native_value False"
    assert singletons.SOL_FALSE.solclass.name == "False", "SOL_FALSE should have class False"

    # 5. ASSERTIONS - Object Model Integrity
    # TODO assert "toString" in object_class.methods or object_class.is_native,
    # "Object class should have methods"

    print("-^-^-^-^-^-^- All tests successful! -^-^-^-^-^-^-^-")

if __name__ == "__main__":
    try:
        test_bootstrap_logic()
    except AssertionError as e:
        print(f"Test failed: {e}")
    except Exception as e:
        print(f"Uknown error: {e}")
