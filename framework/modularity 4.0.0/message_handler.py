from PySide6.QtCore import (
    QCoreApplication, Qt, qInstallMessageHandler, QtMsgType, qDebug, 
    QMessageLogContext)
from typing import Callable, TextIO
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from datetime import datetime
import inspect
from os.path import basename
from enum import Enum
import sys
from config import APP_UNSTABLE, APP_TITLE, APP_VERSION, APP_BUILD_MODE

__all__ = [
    "message_handler",
    "VerboseMode",
]


def _getContext(callFrame) -> tuple[str, int, str]:
    frameInfo = inspect.getframeinfo(callFrame)
    lineNumber = frameInfo.lineno

    filepath = basename(frameInfo.filename)
    return filepath, lineNumber

def _formatContext(callFrame) -> str:
    filename, lineNumber = _getContext(callFrame)
    
    return '%s:%s' % (filename, lineNumber)

def _formatTime() -> str:
    now = datetime.now()
    formatted = now.strftime('%H:%M:%S.%f')[:-3]
    return ' at %s' % formatted

def _formatMsgType(msgType: QtMsgType) -> str:
    match msgType:
        case QtMsgType.QtInfoMsg:
            return f"{Fore.BLUE}INFO{Style.RESET_ALL}"
        case QtMsgType.QtWarningMsg:
            return f"{Fore.YELLOW}WARNING{Style.RESET_ALL}"
        case QtMsgType.QtCriticalMsg:
            return f"{Fore.RED}CRITICAL{Style.RESET_ALL}"
        case QtMsgType.QtFatalMsg:
            return f"{Fore.MAGENTA}FATAL{Style.RESET_ALL}"
        case _:
            return f"{Fore.LIGHTGREEN_EX}DEBUG{Style.RESET_ALL}"

def _formatMsgColor(message: str, msgType: QtMsgType) -> str:
    message = Style.BRIGHT + message
    
    match msgType:
        case QtMsgType.QtInfoMsg:
            return Fore.BLUE + message + Style.RESET_ALL
        case QtMsgType.QtWarningMsg:
            return Fore.YELLOW + message + Style.RESET_ALL
        case QtMsgType.QtCriticalMsg:
            return Fore.RED + message + Style.RESET_ALL
        case QtMsgType.QtFatalMsg:
            return Fore.MAGENTA + message + Style.RESET_ALL
        case _:
            return Fore.LIGHTGREEN_EX + message + Style.RESET_ALL


def low(message: str, msgType: QtMsgType) -> str:
    return _formatMsgType(msgType) + ": " + Style.BRIGHT + message + Style.RESET_ALL

def medium(message: str, msgType: QtMsgType, callFrame) -> str:
    return _formatMsgType(msgType) + " |" + Style.DIM + _formatContext(callFrame) + Style.RESET_ALL + ": " + _formatMsgColor(message, msgType)

def high(message: str, msgType: QtMsgType, callFrame) -> str:
    return _formatMsgType(msgType) + " |" + Style.DIM + _formatContext(callFrame) + _formatTime() + Style.RESET_ALL + ": " + _formatMsgColor(message, msgType)


class VerboseMode(Enum):
    SILENT = 0X00
    NULL = SILENT
    LOW = 0X10
    MEDIUM = 0X20
    HIGH = 0X30


def message_handler(verbose: VerboseMode | int = VerboseMode.LOW, /, 
                    prefix: str = "\t", 
                    output: TextIO = sys.stdout
                    ) -> Callable[[QtMsgType, QMessageLogContext, str], None]:
    colorama_init()
    
    def message_format(msgType: QtMsgType, context: QMessageLogContext, message: str):
        callFrame = inspect.currentframe().f_back

        render: str = prefix

        match(verbose):
            case VerboseMode.LOW:
                render += low(message, msgType)
            case VerboseMode.MEDIUM:
                render += medium(message, msgType, callFrame)
            case VerboseMode.HIGH:
                render += high(message, msgType, callFrame)
            case _:
                return
        
        print(render, file=output)

    if APP_UNSTABLE:
        print(f"{APP_TITLE} [Version {APP_VERSION}.{APP_BUILD_MODE}]")
        message_format(QtMsgType.QtInfoMsg, None, f"Launching on {verbose.name} verbose{_formatTime()}")

    return message_format
