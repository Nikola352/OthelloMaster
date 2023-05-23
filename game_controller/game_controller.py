from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from game_controller.constants import BLACK, WHITE, EMPTY

class GameController(QObject):

    update_game_state_signal = pyqtSignal(list, int, tuple)
    update_available_moves_signal = pyqtSignal(list)
    move_skipped_signal = pyqtSignal()
    game_over_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._board = [[EMPTY]*8 for _ in range(8)]
        self._turn = BLACK
        self._black_score = 0
        self._white_score = 0

    def _set_initial_board(self):
        self._board = [[EMPTY]*8 for _ in range(8)]
        self._board[3][3] = WHITE
        self._board[3][4] = BLACK
        self._board[4][3] = BLACK
        self._board[4][4] = WHITE

    @pyqtSlot(int, int)
    def board_square_selected(self, i, j):
        self._board[i][j] = self._turn
        self._turn = -self._turn
        self.update_game_state_signal.emit(self._board, self._turn, (self._black_score, self._white_score))

    @pyqtSlot(str, str, str)
    def start_game(self, mode, player_color, difficulty):
        print(mode, player_color, difficulty)
        self._set_initial_board()
        self.update_game_state_signal.emit(self._board, self._turn, (self._black_score, self._white_score))

    @pyqtSlot()
    def undo(self):
        pass

    @pyqtSlot()
    def redo(self):
        pass