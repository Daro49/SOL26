# test_sol_model.py
from interpreter.objectModel.sol_class import SolClass
from interpreter.objectModel.sol_method import SolMethod

def test_sol_class_lookup():
    print("Starting tests for SolClass...")

    # 1. SETUP: Class hierarachy
    # Object as root
    obj_class = SolClass(name="Object", superclass=None)
    obj_class.methods["toString"] = SolMethod(selector="toString", params=[], native_function=lambda: "an Object")

    # Animal < Object
    animal_class = SolClass(name="Animal", superclass=obj_class)
    animal_class.methods["eat"] = SolMethod(selector="eat", params=[], native_function=lambda: "nom nom")

    # Dog < Animal
    dog_class = SolClass(name="Dog", superclass=animal_class)
    dog_class.methods["bark"] = SolMethod(selector="bark", params=[], native_function=lambda: "woof!")

    # 2. ASSERT: Functionality
    
    # Test A: Method in same class
    method = dog_class.lookup_method("bark")
    assert method is not None, "Dog should bark"
    assert method.selector == "bark"

    # Test B: Find method in super
    method = dog_class.lookup_method("eat")
    assert method is not None, "Dog should inherit eat from Animal"
    assert method.selector == "eat"

    # Test C: Find method in super super
    method = dog_class.lookup_method("toString")
    assert method is not None, "Dog should inherit toString from Object"

    # Test D: Nonexistent method
    method = dog_class.lookup_method("fly")
    assert method is None, "Dog should not have method fly"

    print("-^-^-^-^-^-^- All tests successful! -^-^-^-^-^-^-^-")

if __name__ == "__main__":
    test_sol_class_lookup()