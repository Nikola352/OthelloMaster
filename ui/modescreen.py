from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget

class ModeScreen(QWidget):
    def __init__(self, stacked_layout, startGameSignal):
        super().__init__()
        self.stacked_layout = stacked_layout
        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.setStyleSheet("background-color: rgb(11, 94, 112)")
        self.initUI()

    def initUI(self):
        pass