from PyQt5.QtWidgets import QMainWindow, QStackedLayout, QWidget
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtCore import pyqtSignal

from ui.gamescreen import GameplayScreen
from ui.modescreen import ModeScreen
from ui.startscreen import StartScreen
from ui.howtoplayscreen import HowToPlayScreen

from game.game_controller import GameController

class MainWindow(QMainWindow):

    def __init__(self, game_controller):
        super(MainWindow, self).__init__()
        self.setGeometry(200, 200, 1000, 600)
        self.setWindowTitle("Othello Master")
        self.setStyleSheet("background-color: rgb(11, 94, 112)")
        self.initUI()
        self.initController(game_controller)

    startGameSignal = pyqtSignal(str, str, str)

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.stacked_layout = QStackedLayout()

        self.start_screen = StartScreen(self.stacked_layout)
        self.howtoplay_screen = HowToPlayScreen(self.stacked_layout)
        self.mode_screen = ModeScreen(self.stacked_layout, self.startGameSignal)
        self.gameplay_screen = GameplayScreen(self.stacked_layout)

        self.stacked_layout.addWidget(self.start_screen)
        self.stacked_layout.addWidget(self.howtoplay_screen)
        self.stacked_layout.addWidget(self.mode_screen)
        self.stacked_layout.addWidget(self.gameplay_screen)
        
        central_widget.setLayout(self.stacked_layout)

    def initController(self, game_controller: GameController):
        self.game_controller = game_controller
        self.game_controller.update_game_state_signal.connect(self.gameplay_screen.updateGameState)
        self.game_controller.update_available_moves_signal.connect(self.gameplay_screen.updateAvailableMoves)
        self.game_controller.game_over_signal.connect(self.gameplay_screen.gameOver)

        self.gameplay_screen.board_square_selected_signal.connect(self.game_controller.board_square_selected)
        self.gameplay_screen.undo_signal.connect(self.game_controller.undo)
        self.gameplay_screen.redo_signal.connect(self.game_controller.redo)
        self.gameplay_screen.resign_signal.connect(self.mode_screen.resetSelection)

        self.startGameSignal.connect(self.game_controller.start_game)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.start_screen.resize(a0.size())
        self.howtoplay_screen.resize(a0.size())
        self.gameplay_screen.resize(a0.size())
        return super().resizeEvent(a0)

