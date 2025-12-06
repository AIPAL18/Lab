from __future__ import annotations

from framework.globals import internal as inal
import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel


@inal.Object
class MyWindow(QMainWindow):
    def __init__(self, label: QLabel):
        QMainWindow.__init__(self)
        self.setStyleSheet("background-color: black; color: white;")
        self.show()
        
        self.label = label
    
    def mousePressEvent(self, event):
        print(self.label.text())
        return QMainWindow.mousePressEvent(self, event)


@inal.Object
class MLabel(QLabel):
    def __init__(self, text: str, parent=None):
        QLabel.__init__(self, text, parent)


# class MLabel(inal.BaseObject, QLabel):
#     def __init__(self, text: str, parent=None):
#         super().__init__(text, parent)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exit_b = QPushButton("Quit")
    exit_b.pressed.connect(app.quit)
    exit_b.show()
    
    w = inal.new(MyWindow)
    l = inal.new(MLabel)
    w(l)
    l("Bonjour", w)

    sys.exit(app.exec())
