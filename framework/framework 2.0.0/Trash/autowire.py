from pyioc3.autowire import bind, AutoWireContainerBuilder
import re


class QuackProvider:
    def quack(self):
        raise NotImplementedError()


@bind()
class Duck:
    def __init__(self, quack: QuackProvider):
        self._quack = quack

    def quack(self):
        self._quack.quack()


@bind(QuackProvider)
class Squeak(QuackProvider):

    def quack(self):
        print("Squeak")


print(__package__, __name__, __dict__)
duck = AutoWireContainerBuilder("__main__").build().get(Duck)
duck.quack()