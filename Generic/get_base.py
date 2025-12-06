from types import GenericAlias


class make_shared[T]:
    def __new__(cls, obj: T) -> T:
        return obj

    @classmethod
    def __class_getitem__(cls, key):
        # https://docs.python.org/3/reference/datamodel.html#object.__class_getitem__
        # print(key)
        # cls.__type = key
        """
        ['__args__', '__call__', '__class__', '__delattr__', '__dir__', '__doc__', 
        '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', 
        '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', 
        '__instancecheck__', '__iter__', '__le__', '__lt__', '__mro_entries__', 
        '__ne__', '__new__', '__or__', '__origin__', '__parameters__', '__reduce__', 
        '__reduce_ex__', '__repr__', '__ror__', '__setattr__', '__sizeof__', 
        '__str__', '__subclasscheck__', '__subclasshook__', 
        '__typing_unpacked_tuple_args__', '__unpacked__']
        """
        return GenericAlias(make_shared, key)


from abc import ABC, abstractmethod


class IApp(ABC):
    @abstractmethod
    def name(self) -> str: ...

class App(IApp):
    def name(self) -> str:
        return self.__class__.__name__


a = make_shared[IApp]
app = a(App())
print(app.__orig_class__)  # __main__.make_shared[__main__.IApp]
print(app.__orig_class__.__origin__)  # <class '__main__.make_shared'>
print(app.__orig_class__.__args__)  # (<class '__main__.IApp'>,)
