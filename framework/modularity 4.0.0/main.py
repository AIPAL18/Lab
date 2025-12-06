import sys
import os
from PySide6.QtCore import (
    QCoreApplication, Qt, qInstallMessageHandler, qDebug)
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication
from config import *
from app.internal.commandlineparser import CommandLineParser
from app.app_factory import AppFactory
from Core.globals.types import IApplication
from message_handler import message_handler, VerboseMode


if __name__ == "__main__" and sys.version_info >= (3, 12):
    if APP_UNSTABLE:
        qInstallMessageHandler(message_handler())
    
    print(sys.argv)
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
        QCoreApplication.setApplicationName("Test_Development")
    else:
        QCoreApplication.setApplicationName("Test")
    QCoreApplication.setOrganizationName("Mon org")
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


"""
Optimiser le tout !!

pip install importtime-waterfall
pip install yelp-gprof2dot
https://graphviz.org/download/

importtime-waterfall main --har

python.exe -m cProfile -o log.pstats main.py run
gprof2dot log.pstats | dot -Tsvg -o log.svg
gprof2dot log.pstats -z gui_app:34:perform | dot -Tsvg -o log.svg
"""
