# Résulats des comparaisons de modularity 1.0.0 et 4.0.0

## Détails

Code de test:

```python
import timeit
import modularity1  # 1.0.0
import modularity2  # 4.0.0


setup_ioc_1 = """
...
"""

setup_ioc_2 = """
...
"""

time_1 = timeit.timeit("test()", setup=setup_ioc_1, number=100_000, globals=modularity1.__dict__)
time_2 = timeit.timeit("test()", setup=setup_ioc_2, number=100_000, globals=modularity2.__dict__)

print(f"1 time: {time_1}")
print(f"2 time: {time_2}")
```

### Test 1: Utilisation de `ioc()`

* Nombre d'exécution: 10_000_000
* Temps ($\delta$=2.6):

| Version | temps (en sec) |
| ------- | -------------- |
| 1.0.0   | 2.580929699994158 sec |
| 4.0.0   | 0.9961545999976806 sec |

<details>
<summary>
Code (1.0.0)
</summary>

```python
def test():
    ioc()
```

</details>

<details>
<summary>
Code (4.0.0)
</summary>

```python
def test():
    ioc()
```

</details>

### Test 2: Utilisation de `registerExport()` et `register()`

* Nombre d'exécution: 100_000
* Temps ($\delta$=1.7):

| Version | temps (en sec) |
| ------- | -------------- |
| 1.0.0   | 8.969312000001082 sec |
| 4.0.0   | 5.2025612000143155 sec |

<details>
<summary>
Code (1.0.0)
</summary>

```python
from typing import override

def test():
    @INTERFACE_ID
    class IUiEngine(ModuleExportInterface): ...

    class UiEngine(IUiEngine): ...

    class UiModule(ModuleExportInterface):
        @override
        @staticmethod
        def moduleName() -> str:
            return "ui"

        @override
        def registerExports(self) -> None:
            ...

        @override
        def resolveImports(self) -> None:
            ...

        @override
        def registerApi(self) -> None:
            ...

        @override
        def registerResources(self) -> None:
            ... 

        @override
        def registerUiTypes(self) -> None:
            ...

        @override
        def onPreInit(self) -> None:
            ...

        @override
        def onInit(self) -> None:
            ...

        @override
        def onAllInited(self) -> None:
            ...

        @override
        def onDeinit(self) -> None:
            ...
    
    ioc().registerExport("ui", UiEngine())
```

</details>

<details>
<summary>
Code (4.0.0)
</summary>

```python
from typing import override

def test():
    class IUiEngine(ModuleInterface): ...

    class UiEngine(IUiEngine): ...

    class UiModule(ModuleSetup):
        @override
        @staticmethod
        def moduleName() -> str:
            return "ui"

        @override
        def registerExports(self) -> None:
            ...

        @override
        def resolveImports(self) -> None:
            ...

        @override
        def registerApi(self) -> None:
            ...

        @override
        def registerResources(self) -> None:
            ... 

        @override
        def registerUiTypes(self) -> None:
            ...

        @override
        def onPreInit(self) -> None:
            ...

        @override
        def onInit(self) -> None:
            ...

        @override
        def onAllInited(self) -> None:
            ...

        @override
        def onDeinit(self) -> None:
            ...
    
    ioc().register(UiEngine, UiEngine())
```

</details>

### Test 3: Utilisation de `resolve()`

* Nombre d'exécution: 10_000_000
* Temps ($\delta$=20.8):

| Version | temps (en sec) |
| ------- | -------------- |
| 1.0.0   | 4.7540624999965075 sec |
| 4.0.0   | 0.22917820001021028 sec |

<details>
<summary>
Code (1.0.0)
</summary>

```python
@INTERFACE_ID
class IOne(ModuleExportInterface): ...
class One(IOne): ...
ioc().registerExport("One", One())

@INTERFACE_ID
class ITwo(ModuleExportInterface): ...
class Two(ITwo): ...
ioc().registerExport("Two", Two())

@INTERFACE_ID
class IThree(ModuleExportInterface): ...
class Three(IThree): ...
ioc().registerExport("Three", Three())

@INTERFACE_ID
class IFour(ModuleExportInterface): ...
class Four(IFour): ...
ioc().registerExport("Four", Four())

@INTERFACE_ID
class IFive(ModuleExportInterface): ...
class Five(IFive): ...
ioc().registerExport("Five", Five())

def test():
    ioc().resolve("One", "", One())
```

</details>

<details>
<summary>
Code (4.0.0)
</summary>

```python
class IOne(ModuleInterface): ...
class One(IOne): ...
ioc().register(One, One())

class ITwo(ModuleInterface): ...
class Two(ITwo): ...
ioc().register(Two, Two())

class IThree(ModuleInterface): ...
class Three(IThree): ...
ioc().register(Three, Three())

class IFour(ModuleInterface): ...
class Four(IFour): ...
ioc().register(Four, Four())

class IFive(ModuleInterface): ...
class Five(IFive): ...
ioc().register(Five, Five())

def test():
    ioc().resolve(IOne)
```

</details>
