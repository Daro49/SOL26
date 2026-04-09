from interpreter.objectModel.sol_class import SolClass
from interpreter.objectModel.sol_object import SolObject
from interpreter.objectModel.sol_method import SolMethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from interpreter.runtime.runtime import Runtime

CLASS_NAME = "Nil"

def register(_class: SolClass, _classes: dict[str, SolClass]) -> None:
    
    def _asString(
        runtime: Runtime,
        receiver: SolObject,
        args: list[SolObject]
        ) -> SolObject:
        
        return SolObject(solclass=_classes.get("String"), native_value="nil")
    
    _class.methods["asString"] = SolMethod(
        [],
        native_function=_asString
    )
