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
        layout = QVBoxLayout(self)

        # Title Label
        self.title_label = QLabel(self)
        self.title_label.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(48)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color: white")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setText("Othello Master")
        layout.addWidget(self.title_label)

        # Buttons
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(self.geometry().width()//5, 0, self.geometry().width()//5, 0)
        
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(24)
        font.setWeight(75)

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)

        # Play Button
        self.play_button = QPushButton(self)
        self.play_button.setFont(font)
        self.play_button.setPalette(palette)
        self.play_button.setObjectName("play_button")
        self.play_button.setText("Play")
        self.play_button.clicked.connect(self.showModeScreen)
        self.verticalLayout.addWidget(self.play_button)

        # How to play Button
        self.how_to_play_button = QPushButton(self)
        font.setPointSize(18)
        self.how_to_play_button.setFont(font)
        self.how_to_play_button.setPalette(palette)
        self.how_to_play_button.setObjectName("how_to_play_button")
        self.how_to_play_button.setText("How to Play")
        self.how_to_play_button.clicked.connect(self.showHowToPlay)
        self.verticalLayout.addWidget(self.how_to_play_button)

        # Exit Button
        self.exit_button = QPushButton(self)
        font.setPointSize(18)
        self.exit_button.setFont(font)
        self.exit_button.setObjectName("exit_button")
        self.exit_button.setText("Exit")
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        self.exit_button.setPalette(palette)
        self.exit_button.clicked.connect(QApplication.instance().quit)
        self.verticalLayout.addWidget(self.exit_button)

        layout.addLayout(self.verticalLayout)
        self.setLayout(layout)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.verticalLayout.setContentsMargins(event.size().width()//5, 0, event.size().width()//5, 0)
        return super().resizeEvent(event)

    def showHowToPlay(self):
        self.stacked_layout.setCurrentIndex(1)

    def showModeScreen(self):
        self.stacked_layout.setCurrentIndex(2)
