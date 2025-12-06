from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal
from PySide6.QtCore import QDir
from PySide6.QtGui import QGuiApplication
# from draw.types.color import Color
# from graphicsapiprovider import GraphicsApiProvider
# from core.ui.view.QmlTranslation import QmlTranslation
from core.ui.IUiEngine import IUiEngine


class QmlApiEngine(QObject):
    def __init__(self, engine):
        super().__init__()
        self.m_engine = engine

    def newQObject(self, obj):
        if obj.parent() is None:
            obj.setParent(self.m_engine)
        return self.m_engine.newQObject(obj)

    def newObject(self):
        return self.m_engine.newObject()

    def newArray(self, length=0):
        return self.m_engine.newArray(length)


class UiEngine(IUiEngine):
    rootItemChanged = Signal(QObject)

    def __init__(self):
        super().__init__()
        self.m_engine = QQmlApplicationEngine()
        self.m_apiEngine = QmlApiEngine(self.m_engine)
        # self.m_translation = QmlTranslation(self)
        # self.m_interactiveProvider = InteractiveProvider(self.iocContext())
        # self.m_api = QmlApi(self, self.iocContext())
        # self.m_tooltip = QmlToolTip(self, self.iocContext())
        # self.m_theme = ThemeApi(self.m_apiEngine)
        self.m_rootItem = None
        self.m_isEffectsAllowed = -1

    def init(self):
        # self.m_theme.init()
        # self.m_tooltip.init()
        self.m_engine.rootContext().setContextProperty("ui", self)
        # self.m_engine.rootContext().setContextProperty("api", self.m_api)

        # qmlIoc = QmlIoCContext(self)
        # qmlIoc.ctx = self.iocContext()
        # self.m_engine.setProperty("ioc_context", QVariant.fromValue(qmlIoc))

        # translator = self.m_engine.newQObject(self.m_translation)
        # translateFn = translator.property("translate")
        # self.m_engine.globalObject().setProperty("qsTrc", translateFn)

        dir_path = QDir(QApplication.applicationDirPath() + "/../qml")
        self.m_engine.addImportPath(dir_path.absolutePath())

        self.m_engine.addImportPath(":/qml")

    def quit(self):
        if not self.m_engine:
            return

        self.m_engine.quit.emit()
        del self.m_engine
        self.m_engine = None

    def rootItem(self):
        return self.m_rootItem

    def setRootItem(self, rootItem):
        if self.m_rootItem == rootItem:
            return

        self.m_rootItem = rootItem
        self.rootItemChanged.emit(self.m_rootItem)

    # def isEffectsAllowed(self):
    #     if self.m_isEffectsAllowed == -1:
    #         self.m_isEffectsAllowed = GraphicsApiProvider.graphicsApi() != GraphicsApiProvider.GraphicsApiPro

    def addSourceImportPath(self, path):
        print(path)  # LOGD() equivalent
        self.m_source_import_paths.append(path)
        if self.m_engine:
            self.m_engine.add_import_path(path)

    def updateTheme(self):
        if not self.m_engine:
            return
        self.theme().update()

    def api(self):
        return self.m_api

    def theme(self):
        return self.m_theme

    def tooltip(self):
        return self.m_tooltip

    def interactiveProvider_property(self):
        return self.m_interactive_provider.get()

    def interactiveProvider(self):
        return self.m_interactive_provider

    def keyboardModifiers(self):
        return QGuiApplication.keyboard_modifiers()

    def currentLanguageLayoutDirection(self):
        return self.languages_service().current_language().direction

    # def blendColors(self, c1, c2):
    #     return draw.blend_q_colors(c1, c2)

    # def blendColors(self, c1, c2, alpha):
    #     return draw.blend_q_colors(c1, c2, alpha)

    def colorWithAlphaF(self, src, alpha):
        c = src.copy()  # Assuming QColor has a copy method
        c.set_alpha_f(alpha)
        return c

    def qmlAppEngine(self):
        return self.m_engine

    def qmlEngine(self):
        return self.qml_app_engine()

    def clearComponentCache(self):
        self.m_engine.clear_component_cache()

    # def graphicsApi(self):
    #     return GraphicsApiProvider.graphics_api()

    # def graphicsApiName(self):
    #     return GraphicsApiProvider.graphics_api_name()