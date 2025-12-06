"""
NOTE: Don't make consts globals https://stackoverflow.com/a/6965111/15793884
"""

import sys
import os
import subprocess
from typing import Final

__all__ = [
    # App macros
    "APP_NAME",
    "APP_ORGANISATION",
    "APP_NAME_MACHINE_READABLE_COMPAT",
    "APP_TITLE",
    "APP_DESCRIPTION",
    "APP_GUI_IDENTIFIER",
    "APP_UNSTABLE",
    "APP_VERSION",
    "APP_VERSION_MAJOR",
    "APP_VERSION_MINOR",
    "APP_VERSION_PATCH",
    "APP_BUILD_MODE",
    "APP_REVISION",
    "APP_INSTALL_PREFIX",
    "APP_INSTALL_NAME",

    # Qt macros
    "Q_OS_WIN",
    "Q_OS_DARWIN",
    "Q_OS_LINUX",
]

# Handlers

def get_git(cmd, *, default: str = "") -> str:
    if os.path.exists(".git"):
        return subprocess.run(cmd, stdout=subprocess.PIPE, text=True).stdout[:-1]

    return default

# App macros
#! NOTE: Remove APP_NAME and APP_TITLE
APP_NAME: Final[str] = "Application_Test"
APP_ORGANISATION: Final[str] = "tester"
APP_NAME_MACHINE_READABLE_COMPAT: Final[str] = "Test"
APP_TITLE: Final[str] = "Application de Test"
APP_DESCRIPTION: Final[str] = "Une application pour tester l'architecture de Musescore Studio"
APP_GUI_IDENTIFIER: Final[str] = f"org.{APP_ORGANISATION}.{APP_NAME_MACHINE_READABLE_COMPAT}"

APP_UNSTABLE: Final[bool] = True
APP_VERSION: Final[str] = "1.0.0"
APP_VERSION_MAJOR: Final[str] = "1"
APP_VERSION_MINOR: Final[str] = "0"
APP_VERSION_PATCH: Final[str] = "0"
APP_BUILD_MODE: Final[str] = "dev" # dev|testing|release
APP_REVISION: Final[str] = get_git("git rev-parse --short=7 HEAD", default="none")

APP_INSTALL_PREFIX: Final[str] = sys.path[0]
APP_INSTALL_NAME: Final[str] = "" 


# Qt macros
Q_OS_WIN: Final[bool] = sys.platform == "win32"      # Windows
Q_OS_DARWIN: Final[bool] = sys.platform == "darwin"  # Mac
Q_OS_LINUX: Final[bool] = sys.platform == "linux"     # Linux


if __name__ == "__main__":
    print(APP_REVISION)
