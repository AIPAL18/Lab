from typing import TypeVar
import ctypes
import gc
import weakref
T = TypeVar("T")


class Object(object):
    __wr = None

    def __init__(self, var):
        self.m_var = var
    
    # def __new__(cls, var):
    #     """
    #     https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/
    #     """
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(Object, cls).__new__(cls)
    #         cls.__wr = weakref.ref(cls.instance)
        
    #     return cls.instance

    # @staticmethod
    def use_count(self):
        """
        https://www.geeksforgeeks.org/weak-references-in-python/
        """
        # return ctypes.c_long.from_address(id(self)).value - 1
        return weakref.getweakrefcount(self)

    def unique(self):
        """
        https://stackoverflow.com/a/9908216
        """
        gc.collect()
        print(self.__wr)
        return self.__wr is None


def ref(obj: Object) -> Object:
    return weakref.ref(obj)


if __name__ == "__main__":
    # https://www.geeksforgeeks.org/weak_ptr-in-cpp/
    c1 = Object(None)
    c2 = ref(c1)
    c3 = ref(c1)
    print(weakref.getweakrefcount(c1))
