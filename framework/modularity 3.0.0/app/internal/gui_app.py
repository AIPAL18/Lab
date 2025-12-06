# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from PySide6.QtCore import QUrl, Qt, QObject, QCoreApplication
from typing import override
from Core.globals.types import BaseApplication, IApplication
from .cmd_options import CmdOptions
from Core.globals.modularity import Inject, ModuleSetup, ioc
from PySide6.QtQuick import QQuickWindow
from PySide6.QtQml import QQmlApplicationEngine, QQmlError
# from appshell.appshell import IAppShellConfiguration
import appshell.appshell_rc
from PySide6.QtCore import QThreadPool
from Core.ui.IUiEngine import IUiEngine


class GuiApp(BaseApplication):   # enable_shared_from_this ???
    application = Inject(IApplication)
    # appshellConfiguration = Inject(IAppShellConfiguration)
    #! TODO: impl them I guess
    # muse::Inject<appshell::IAppShellConfiguration> appshellConfiguration;
    # muse::Inject<appshell::IStartupScenario> startupScenario;

    def __init__(self: GuiApp, options: CmdOptions):
        super().__init__()
        self.options = options
        self.__modules: list[ModuleSetup] = []
        # self.__globalModule = GlobalModule()
        
    def addModule(self: GuiApp, module: ModuleSetup):
        self.__modules.append(module)
    
    @override
    def perform(self):
        options = self.options

        runMode = options.runMode
        if runMode != IApplication.RunMode.GuiApp:
            print("GuiApp's runMode is not GuiApp !!")
            return

        self.setRunMode(runMode)
        # self.__globalModule.setApplication(self.shared_from_this())  # enable_shared_from_this donc...
        # self.__globalModule.registerResources()
        # self.__globalModule.registerExports()
        # self.__globalModule.registerUiTypes()

        for m in self.__modules:
            # m.setApplication()  # don't exist ??? WTF, he had a lot of new things in there
            m.registerResources()
        
        for m in self.__modules:
            m.registerExports()
        
        # self.__globalModule.resolveImports()
        # self.__globalModule.registerApi()
        
        for m in self.__modules:
            m.registerUiTypes()
            m.resolveImports()
            m.registerApi()  #! TODO: obviously...
        
        self.__applyCommandLineOptions(options)

        # self.__globalModule.onPreInit()
        for m in self.__modules:
            m.onPreInit(runMode)
        
        # SplashScreen here: unnecessary for this project

        # self.__globalModule.onInit()
        for m in self.__modules:
            m.onInit(runMode)
        
        # self.__globalModule.onAllInited()
        for m in self.__modules:
            m.onAllInited(runMode)
        
        """
        QMetaObject::invokeMethod(qApp, [this]() {
            m_globalModule.onStartApp();
            for (modularity::IModuleSetup* m : m_modules) {
                m->onStartApp();
            }
        }, Qt::QueuedConnection);
        """
        # self.__globalModule.onStartApp()
        for m in self.__modules:
            m.onStartApp()
        
        #! Needs to be set because we use transparent windows for PopupView.
        #! Needs to be called before any QQuickWindows are shown.
        QQuickWindow.setDefaultAlphaBuffer(True)

        engine = ioc().resolve(IUiEngine, "app", "").qmlAppEngine()

        main_qml_file = "Main.qml"
        url = QUrl("qrc:/qml/" + main_qml_file)

        # I don't know what it's about...
        def func(obj: QObject, url: QUrl):
            w: QQuickWindow = obj
            def inner(type: QQuickWindow.SceneGraphError, msg: str):
                print(f"scene graph error: {msg}")
            w.sceneGraphError.connect(inner)

        engine.objectCreated.connect(func, Qt.ConnectionType.DirectConnection)

        # I still don't know what it's about...
        def func2(obj: QObject, objUrl: QUrl):
            if not obj and url == objUrl:
                print("failed Qml load!")
                QCoreApplication.exit(-1)
                return
            if url == objUrl:
                # ====================================================
                # Setup modules: onDelayedInit
                # ====================================================
                # self.__globalModule.onDelayedInit()
                for m in self.__modules:
                    m.onDelayedInit()
            
            # if splashScreen:
            #     splashScreen.close()
            #     del splashScreen
        
        engine.objectCreated.connect(func2, Qt.ConnectionType.QueuedConnection)

        def engine_warnings(warnings: list[QQmlError]):
            for error in warnings:
                print(f"error: {error.toString()}")
        
        engine.warnings.connect(engine_warnings)

        engine.load(url)
            
    @override
    def finish(self):
        globalThreadPool = QThreadPool.globalInstance()
        if globalThreadPool:
            globalThreadPool.waitForDone()
        
        ioc().resolve(IUiEngine, "app", "").quit()

        for m in self.__modules:
            m.onDeinit()
        
        for m in self.__modules:
            m.onDestroy()
        
        self.__modules.clear()

    
    def __applyCommandLineOptions(self: GuiApp, options: CmdOptions):
        ...
