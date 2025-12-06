from __future__ import annotations

import modularity as mod
import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel


@mod.Object
class MyWindow(QMainWindow):
    def __init__(self, label: QLabel):
        QMainWindow.__init__(self)
        self.setStyleSheet("background-color: black; color: white;")
        self.show()
        
        self.label = label
    
    def mousePressEvent(self, event):
        print(self.label.text())
        return QMainWindow.mousePressEvent(self, event)


@mod.Object
class MLabel(QLabel):
    def __init__(self, text: str, parent=None):
        QLabel.__init__(self, text, parent)


# class MLabel(mod.BaseObject, QLabel):
#     def __init__(self, text: str, parent=None):
#         super().__init__(text, parent)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exit_b = QPushButton("Quit")
    exit_b.pressed.connect(app.quit)
    
    try:
        w = mod.new(MyWindow)
        l = mod.new(MLabel)
        w(l)
        l("Bonjour", w)
    except:
        exit_b.show()

    sys.exit(app.exec())
