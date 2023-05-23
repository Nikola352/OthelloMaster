import random
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QButtonGroup
from PyQt5.QtGui import QIcon, QPixmap, QFont, QPalette, QResizeEvent

class ModeScreen(QWidget):
    def __init__(self, stacked_layout, startGameSignal):
        super().__init__()
        self.stacked_layout = stacked_layout
        self.setLayoutDirection(Qt.LeftToRight)
        self.setStyleSheet("background-color: rgb(11, 94, 112)")
        self.initUI()
        self.startGameSignal = startGameSignal
        self.mode = "single_player"
        self.difficulty = "hard"
        self.player = random.choice(["black", "white"])

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(30)
        self.layout.setContentsMargins(self.geometry().width()//5, 0, self.geometry().width()//5, 0)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer)

        # Title Label
        self.title_label = QLabel(self)
        self.title_label.setMaximumHeight(100)
        font = QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(32)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color: white")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setText("Game mode")
        self.layout.addWidget(self.title_label)

        # Buttons
        
        font = QFont()
        font.setBold(True)
        font.setPointSize(24)
        font.setWeight(75)

        palette = QPalette()
        palette.setColor(QPalette.ButtonText, Qt.white)

        spacer1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer1)

        # Mode choice
        mode_choice_layout = QHBoxLayout()
        mode_choice_layout.setSpacing(30)
        mode_choice_layout.setContentsMargins(0, 0, 0, 0)
        mode_choice_layout.setAlignment(Qt.AlignCenter)

        self.difficulty_button_group = QButtonGroup()
        self.difficulty_button_group.setExclusive(True)

        # Single player Button
        pixmap = QPixmap("ui/assets/user_vs_robot.png").scaledToHeight(70)
        self.single_player_button = QPushButton(self)
        self.single_player_button.setIcon(QIcon(pixmap))
        self.single_player_button.clicked.connect(lambda: self.setMode("single_player"))
        self.single_player_button.setCheckable(True)
        self.single_player_button.setChecked(True)
        self.single_player_button.setStyleSheet("QPushButton:checked { border: 2px solid rgb(0, 50, 100); }")
        self.single_player_button.setMinimumSize(70, 70)
        self.single_player_button.setIconSize(self.single_player_button.size())
        self.difficulty_button_group.addButton(self.single_player_button)
        mode_choice_layout.addWidget(self.single_player_button)

        self.layout.addLayout(mode_choice_layout)

        # Two player Button
        pixmap = QPixmap("ui/assets/user_vs_user.png").scaledToHeight(70)
        self.two_player_button = QPushButton(self)
        self.two_player_button.setIcon(QIcon(pixmap))
        self.two_player_button.clicked.connect(lambda: self.setMode("two_player"))
        self.two_player_button.setCheckable(True)
        self.two_player_button.setStyleSheet("QPushButton:checked { border: 2px solid rgb(0, 50, 100); }")
        self.two_player_button.setMinimumSize(70, 70)
        self.two_player_button.setIconSize(self.two_player_button.size())
        self.difficulty_button_group.addButton(self.two_player_button)
        mode_choice_layout.addWidget(self.two_player_button)

        # Player choice
        player_choice_layout = QHBoxLayout()
        player_choice_layout.setSpacing(20)
        player_choice_layout.setContentsMargins(0, 0, 0, 0)
        player_choice_layout.setAlignment(Qt.AlignCenter)

        self.player_button_group = QButtonGroup()

        # Black Button
        pixmap = QPixmap("ui/assets/black.png")
        self.black_button = QPushButton(self)
        self.black_button.setIcon(QIcon(pixmap))
        self.black_button.clicked.connect(lambda: self.setPlayer("black"))
        self.black_button.setCheckable(True)
        self.black_button.setStyleSheet("QPushButton:checked { border: 2px solid rgb(0, 50, 100); }")
        self.black_button.setMinimumSize(70, 70)
        self.black_button.setIconSize(self.black_button.size())
        self.player_button_group.addButton(self.black_button)
        player_choice_layout.addWidget(self.black_button)

        # Random Button
        pixmap = QPixmap("ui/assets/random.png").scaledToHeight(70)
        self.random_button = QPushButton(self)
        self.random_button.setFixedSize(70, 70)
        self.random_button.setIcon(QIcon(pixmap))
        self.random_button.clicked.connect(lambda: self.setPlayer("random"))
        self.random_button.setCheckable(True)
        self.random_button.setChecked(True)
        self.random_button.setStyleSheet("QPushButton:checked { border: 2px solid rgb(0, 50, 100); }")
        self.random_button.setMinimumSize(70, 70)
        self.random_button.setIconSize(self.random_button.size())
        self.player_button_group.addButton(self.random_button)
        player_choice_layout.addWidget(self.random_button)

        # White Button
        pixmap = QPixmap("ui/assets/white.png").scaledToHeight(70)
        self.white_button = QPushButton(self)
        self.white_button.setIcon(QIcon(pixmap))
        self.white_button.clicked.connect(lambda: self.setPlayer("white"))
        self.white_button.setCheckable(True)
        self.white_button.setStyleSheet("QPushButton:checked { border: 2px solid rgb(0, 50, 100); }")
        self.white_button.setMinimumSize(70, 70)
        self.white_button.setIconSize(self.white_button.size())
        self.player_button_group.addButton(self.white_button)
        player_choice_layout.addWidget(self.white_button)

        self.layout.addLayout(player_choice_layout)

        # Difficulty choice
        difficulty_choice_layout = QHBoxLayout()
        difficulty_choice_layout.setSpacing(20)
        difficulty_choice_layout.setContentsMargins(0, 0, 0, 0)
        difficulty_choice_layout.setAlignment(Qt.AlignCenter)

        self.difficulty_button_group = QButtonGroup()

        # Easy Button
        self.easy_button = QPushButton(self)
        self.easy_button.setFont(font)
        self.easy_button.setPalette(palette)
        self.easy_button.setText("Easy")
        self.easy_button.clicked.connect(lambda: self.setDifficulty("easy"))
        self.easy_button.setCheckable(True)
        self.easy_button.setStyleSheet("QPushButton:checked { border: 2px solid rgb(0, 50, 100); }")
        self.difficulty_button_group.addButton(self.easy_button)
        difficulty_choice_layout.addWidget(self.easy_button)

        # Medium Button
        self.medium_button = QPushButton(self)
        self.medium_button.setFont(font)
        self.medium_button.setPalette(palette)
        self.medium_button.setText("Medium")
        self.medium_button.clicked.connect(lambda: self.setDifficulty("medium"))
        self.medium_button.setCheckable(True)
        self.medium_button.setStyleSheet("QPushButton:checked { border: 2px solid rgb(0, 50, 100); }")
        self.difficulty_button_group.addButton(self.medium_button)
        difficulty_choice_layout.addWidget(self.medium_button)

        # Hard Button
        self.hard_button = QPushButton(self)
        self.hard_button.setFont(font)
        self.hard_button.setPalette(palette)
        self.hard_button.setText("Hard")
        self.hard_button.clicked.connect(lambda: self.setDifficulty("hard"))
        self.hard_button.setCheckable(True)
        self.hard_button.setChecked(True)
        self.hard_button.setStyleSheet("QPushButton:checked { border: 2px solid rgb(0, 50, 100); }")
        self.difficulty_button_group.addButton(self.hard_button)
        difficulty_choice_layout.addWidget(self.hard_button)

        self.layout.addLayout(difficulty_choice_layout)

        # Play Button
        self.play_button = QPushButton(self)
        self.play_button.setFont(font)
        self.play_button.setPalette(palette)
        self.play_button.setText("Play")
        self.play_button.clicked.connect(self.showGameplay)
        self.layout.addWidget(self.play_button)

        # Back Button
        self.back_button = QPushButton(self)
        self.back_button.setFont(font)
        self.back_button.setPalette(palette)
        self.back_button.setText("Back")
        self.back_button.clicked.connect(self.showStartScreen)
        self.layout.addWidget(self.back_button)

        spacer3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer3)

        self.setLayout(self.layout)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.layout.setContentsMargins(event.size().width()//5, 0, event.size().width()//5, 0)
        return super().resizeEvent(event)

    def showStartScreen(self):
        self.stacked_layout.setCurrentIndex(0)

    def setMode(self, mode):
        self.mode = mode
        if mode == "single_player":
            self.black_button.setEnabled(True)
            self.random_button.setEnabled(True)
            self.white_button.setEnabled(True)
            self.easy_button.setEnabled(True)
            self.medium_button.setEnabled(True)
            self.hard_button.setEnabled(True)
        else:
            self.black_button.setEnabled(False)
            self.random_button.setEnabled(False)
            self.white_button.setEnabled(False)
            self.easy_button.setEnabled(False)
            self.medium_button.setEnabled(False)
            self.hard_button.setEnabled(False)
        print(self.mode)

    def setPlayer(self, player):
        if player == "random":
            self.player = random.choice(["black", "white"])
        else:
            self.player = player

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty

    def showGameplay(self):
        self.stacked_layout.setCurrentIndex(3)
        self.startGameSignal.emit(self.mode, self.player, self.difficulty)

    @pyqtSlot()
    def resetSelection(self):
        self.mode = "single_player"
        self.player = random.choice(["black", "white"])
        self.difficulty = "hard"
        self.single_player_button.setChecked(True)
        self.random_button.setChecked(True)
        self.hard_button.setChecked(True)
