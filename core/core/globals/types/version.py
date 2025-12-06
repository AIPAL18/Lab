# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from ..multipledispatch import dispatch

__all__ = [
    "SUFFIX_DELIMITER",
    "Version"
]

SUFFIX_DELIMITER = " - "


class Version(object):
    __major: int = 0
    __minor: int = 0
    __patch: int = 0
    __suffix: str = ""
    __suffixVersion: int = 0

    @dispatch(int, int, int, str, int)
    def __init__(
            self: Version, 
            major: int,
            minor: int,
            patch: int,
            suffix: str = "",
            suffixVersion: int = 0
    ) -> None:
        self.__major = major
        self.__minor = minor
        self.__patch = patch
        self.__suffix = suffix
        self.__suffixVersion = suffixVersion

    @dispatch(str)
    def __init__(
        self: Version,
        version_str: str
    ) -> None:
        # ver_suf[0] -> version | ver_suf[1] -> suffix
        ver_suf = version_str.split(SUFFIX_DELIMITER, 1)

        result = ver_suf[0].split(".", 2)
        if len(result) != 3:
            return
        if not all([elem.isnumeric() for elem in result]):
            return
        
        self.__major = int(result[0])
        self.__minor = int(result[1])
        self.__patch = int(result[2])

        if len(ver_suf) == 1:
            return
        
        self.setSuffix(ver_suf[1])

    def major(self: Version) -> int:
        return self.__major

    def minor(self: Version) -> int:
        return self.__minor

    def patch(self: Version) -> int:
        return self.__patch

    def suffix(self: Version) -> str:
        return self.__suffix
    
    def suffixVersion(self: Version) -> int:
        return self.__suffixVersion

    def setSuffix(self: Version, suffix: str) -> None:
        result = suffix.split(".", 1)

        if len(result) == 0:
            return
        
        self.__suffix = result[0]
        if len(result) < 2 or not result[1].isnumeric():
            self.__suffixVersion = 0
            return
        
        self.__suffixVersion = int(result[1])

    def preRelease(self: Version) -> bool:
        return len(self.suffix()) != 0

    def toString(self: Version) -> str:
        result = "{}.{}.{}".format(self.__major, self.__minor, self.__patch)
        if self.__suffix:
            result += SUFFIX_DELIMITER + self.__suffix
            if self.__suffixVersion > 0:
                result += "." + str(self.__suffixVersion)
        
        return result
    
    def __str__(self) -> str:
        return self.toString()

    def __lt__(self: Version, other: Version) -> bool:
        if self.__major > other.major():
            return False
        elif self.__major == other.major():
            if self.__minor > other.minor():
                return False
            elif self.__minor == other.minor():
                if self.__patch > other.patch():
                    return False
                elif self.__patch == other.patch():
                    if not self.__suffix:
                        return False
                    if not other.suffix():
                        return True
                    
                    suffixes = [
                        u"poc",
                        u"dev",
                        u"alpha",
                        u"beta",
                        u"rc"
                    ]
                    if not (self.__suffix in suffixes and other.suffix() in suffixes):
                        print(f"Invalid version suffix; current {self.__suffix}, update {other.suffix()}")
                        return False  # security !
                    
                    current_index = suffixes.index(self.__suffix)
                    update_index = suffixes.index(other.suffix())
                    if current_index < update_index:
                        return True
                    if current_index == update_index:
                        return self.__suffixVersion < other.suffixVersion()
        
        return True
    
    def __eq__(self: Version, other: Version) -> bool:
        return (self.__major == other.major()
            and self.__minor == other.minor()
            and self.__patch == other.patch()
            and self.__suffix == other.suffix()
            and self.__suffixVersion == other.suffixVersion())
    
    def __le__(self: Version, other: Version) -> bool:
        if self == other:
            return True
        
        return self < other


if __name__ == "__main__":
    v = Version(1, 1, 1, "alpha", 1)
    u = Version(1, 1, 1, "b", 2)
    print(v < u)
