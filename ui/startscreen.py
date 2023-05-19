from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication

class StartScreen(QWidget):
    def __init__(self, stacked_layout):
        super().__init__()
        self.stacked_layout = stacked_layout
        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.setStyleSheet("background-color: rgb(11, 94, 112)")
        self.initUI()

    def initUI(self):
        pass