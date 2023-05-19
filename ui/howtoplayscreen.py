from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class HowToPlayScreen(QWidget):
    def __init__(self, stacked_layout):
        super().__init__()
        self.stacked_layout = stacked_layout
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Title Label
        self.title_label = QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(32)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color: white")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setText("How to Play")
        layout.addWidget(self.title_label)

        # Back Button
        self.back_button = QPushButton(self)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.back_button.setFont(font)
        self.back_button.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(11, 94, 112);")
        self.back_button.setText("Back")
        self.back_button.clicked.connect(self.showStartScreen)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def showStartScreen(self):
        self.stacked_layout.setCurrentIndex(0)

    def showGameScreen(self):
        self.stacked_layout.setCurrentIndex(2)