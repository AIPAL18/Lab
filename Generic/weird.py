# from typing import Generic, TypeVar

# T = TypeVar("T")

# class shared_ptr(Generic[T]):
#     def __new__(cls, obj):
#         inst = super().__new__(cls)
#         print("In __new__", hasattr(inst, "__orig_class__"))  # False
#         return inst
    
#     def __init__(self, obj):
#         self.obj = obj
#         print("In __init__", hasattr(self, "__orig_class__"))  # False



# class Foo: ...

# foo = shared_ptr[Foo](Foo())
# print("After construction:", foo.__orig_class__)

from typing import Generic, TypeVar

T = TypeVar("T")

class shared_ptr(Generic[T]):
    def __init__(self, obj: T):
        self.obj = obj
        try:
            print(f"[OK] __orig_class__ =", self.__orig_class__)
            print(f"[OK] Type paramétré =", self.__orig_class__.__args__[0])
        except AttributeError:
            print("[FAIL] __orig_class__ non défini")

class Foo: ...

ptr = shared_ptr[Foo](Foo())  # <- ici, __orig_class__ est bien injecté automatiquement


