# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

import sys

__all__ = [
    # App macros
    "APP_NAME",
    "APP_TITLE",
    "APP_UNSTABLE",
    "APP_VERSION",
    "APP_VERSION_MAJOR",
    "APP_VERSION_MINOR",
    "APP_VERSION_PATCH",
    "APP_INSTALL_PREFIX",
    "APP_INSTALL_NAME",

    # Qt macros
    "Q_OS_WIN",
    "Q_OS_DARWIN",
    "Q_OS_LINUX",
]

# App macros
#! NOTE: Remove APP_NAME and APP_TITLE
APP_NAME = "Jeu-de-la-vie"
APP_TITLE = "Jeu de la vie"

APP_UNSTABLE = True
APP_VERSION = "1.0.0"
APP_VERSION_MAJOR = "1"
APP_VERSION_MINOR = "0"
APP_VERSION_PATCH = "0"

APP_INSTALL_PREFIX = sys.path[0]
APP_INSTALL_NAME = "" 


# Qt macros
Q_OS_WIN = sys.platform == "win32"      # Windows
Q_OS_DARWIN = sys.platform == "darwin"  # Mac
Q_OS_LINUX = sys.platform == "linux"     # Linux
