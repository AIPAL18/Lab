# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

import sys
import os
from PySide6.QtCore import (
    QCoreApplication, Qt, qInstallMessageHandler, QtMsgType)
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication
from config import *
from app.internal.commandlineparser import CommandLineParser
from app.app_factory import AppFactory
from new_source.app.IApplication import IApplication


def qt_message_handler(mode, context, message):
    if mode == QtMsgType.QtInfoMsg:
        mode = "INFO"
    elif mode == QtMsgType.QtWarningMsg:
        mode = "WARNING"
    elif mode == QtMsgType.QtCriticalMsg:
        mode = "CRITICAL"
    elif mode == QtMsgType.QtFatalMsg:
        mode = "FATAL"
    else:
        mode = "DEBUG"
    print(f"\t{mode} {"_" * (10 - len(mode))} {message}")


if __name__ == "__main__" and sys.version_info >= (3, 12):
    qInstallMessageHandler(qt_message_handler)
    
    # ====================================================
    # Setup global Qt application variables
    # ====================================================
    os.putenv("QT_STYLE_OVERRIDE", "Fusion")
    os.putenv("QML_DISABLE_DISK_CACHE", "true")  # True or true ?
    if Q_OS_LINUX:
        if os.getenv("QT_QPA_PLATFORM") != "offscreen":
            os.putenv("QT_QPA_PLATFORMTHEME", "gtk3")
    
    if Q_OS_LINUX:
        QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.RoundPreferFloor)
    elif Q_OS_WIN:
        QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    QGuiApplication.styleHints().setMousePressAndHoldInterval(250)

    if APP_UNSTABLE:
        QCoreApplication.setApplicationName("Jeu-de-la-vie_Development")
    else:
        QCoreApplication.setApplicationName("Jeu-de-la-vie")
    # QCoreApplication.setOrganizationName("")
    QCoreApplication.setApplicationVersion(APP_VERSION)

    # ====================================================
    # Parse command line options
    # ====================================================
    commandLineParser = CommandLineParser()
    commandLineParser.init()
    commandLineParser.parse(len(sys.argv), sys.argv)

    runMode = commandLineParser.runMode()

    qapp = QApplication(sys.argv)

    commandLineParser.processBuiltinArgs(qapp)
    
    factory = AppFactory()
    app: IApplication = factory.newApp(commandLineParser.options())
    
    app.perform()

    # ====================================================
    # Run main loop
    # ====================================================
    code: int = qapp.exec()
        
    # ====================================================
    # Quit
    # ====================================================

    app.finish()

    del qapp

    sys.exit(code)
