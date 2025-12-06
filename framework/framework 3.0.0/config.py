# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

import sys
import os
import subprocess

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
APP_NAME = "Application_Test"
APP_ORGANISATION = "tester"
APP_NAME_MACHINE_READABLE_COMPAT = "Test"
APP_TITLE = "Application de Test"
APP_DESCRIPTION = "Une application pour tester l'architecture de Musescore Studio"
APP_GUI_IDENTIFIER = f"org.{APP_ORGANISATION}.{APP_NAME_MACHINE_READABLE_COMPAT}"

APP_UNSTABLE = True
APP_VERSION = "1.0.0"
APP_VERSION_MAJOR = "1"
APP_VERSION_MINOR = "0"
APP_VERSION_PATCH = "0"
APP_BUILD_MODE = "dev" # dev|testing|release
APP_REVISION = get_git("git rev-parse --short=7 HEAD", default="none")

APP_INSTALL_PREFIX = sys.path[0]
APP_INSTALL_NAME = "" 


# Qt macros
Q_OS_WIN = sys.platform == "win32"      # Windows
Q_OS_DARWIN = sys.platform == "darwin"  # Mac
Q_OS_LINUX = sys.platform == "linux"     # Linux


if __name__ == "__main__":
    print(APP_REVISION)
