from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from ai.random_strategy import RandomStrategy
from ai.greedy_strategy import GreedyStrategy
from ai.minimax_strategy import MinimaxStrategy
from game.util import get_possible_moves, calculate_board_position, get_score
from game.constants import BLACK, WHITE, EMPTY
from util.stack import Stack

import threading

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
        self._get_black_move = None
        self._get_white_move = None
        self._back_stack = Stack(64)
        self._forw_stack = Stack(64)

    def _set_initial_board(self):
        self._board = [[EMPTY]*8 for _ in range(8)]
        self._board[3][3] = WHITE
        self._board[3][4] = BLACK
        self._board[4][3] = BLACK
        self._board[4][4] = WHITE

    @pyqtSlot(str, str, str)
    def start_game(self, mode, player_color, difficulty):
        self._mode = mode
        self._set_initial_board()
        self._turn = BLACK
        self._white_score = self._black_score = 0
        self._back_stack.clear()
        self._forw_stack.clear()
        self.update_game_state_signal.emit(self._board, self._turn, (self._black_score, self._white_score))
        self.update_available_moves_signal.emit([])
        if mode == "two_player":
            self._get_black_move = self._user_move
            self._get_white_move = self._user_move
        elif mode == "single_player":
            if difficulty == "easy":
                self._cpu_strategy = RandomStrategy()
            elif difficulty == "medium":
                self._cpu_strategy = GreedyStrategy()
            elif difficulty == "hard":
                self._cpu_strategy = MinimaxStrategy()

            if player_color == "black":
                self._get_black_move = self._user_move
                self._get_white_move = self._computer_move
            elif player_color == "white":
                self._get_black_move = self._computer_move
                self._get_white_move = self._user_move
        self._next_move()

    def _next_move(self):
        if len(get_possible_moves(self._board, self._turn)) == 0:
            if len(get_possible_moves(self._board, -self._turn)) == 0:
                self.game_over()
                return
            else:
                self.move_skipped_signal.emit()
                self._turn = -self._turn
                self._next_move()
                return
        if self._turn == 1:
            self._get_black_move()
        elif self._turn == -1:
            self._get_white_move()

    @pyqtSlot(int, int)
    def board_square_selected(self, i: int, j: int):
        self.update_available_moves_signal.emit([])
        self._play((i,j))

    def _user_move(self):
        possible_moves = get_possible_moves(self._board, self._turn)
        self.update_available_moves_signal.emit(possible_moves)

    def _computer_move(self):
        def calculate_move():
            move = self._cpu_strategy.get_move(self._board, self._turn)
            self._play(move)
        self.thread = threading.Thread(target=calculate_move)
        self.thread.start()
    
    def _play(self, move: tuple[int,int]):
        self._back_stack.push(self._board)
        self._forw_stack.clear()
        self._board = calculate_board_position(self._board, self._turn, move)
        self._turn = -self._turn
        self._black_score, self._white_score = get_score(self._board)
        self.update_game_state_signal.emit(self._board, self._turn, (self._black_score, self._white_score))
        self._next_move()

    def undo_once(self):
        if self._back_stack.is_empty():
            return
        self._forw_stack.push(self._board)
        self._board = self._back_stack.pop()
        self._turn = -self._turn

    @pyqtSlot()
    def undo(self):
        if self._mode == "two_player":
            self.undo_once()
        elif self._mode == "single_player":
            # wait for computer to play the move
            if self.thread and self.thread.is_alive():
                self.thread.join()
            # undo both computer and user move
            self.undo_once()
            self.undo_once()
        else:
            return
        self._black_score, self._white_score = get_score(self._board)
        self.update_game_state_signal.emit(self._board, self._turn, (self._black_score, self._white_score))
        self.update_available_moves_signal.emit([])
        self._next_move()

    def redo_once(self):
        if self._forw_stack.is_empty():
            return
        self._back_stack.push(self._board)
        self._board = self._forw_stack.pop()
        self._turn = -self._turn

    @pyqtSlot()
    def redo(self):
        if self._mode == "two_player":
            self.redo_once()
        elif self._mode == "single_player":
            # wait for computer to play the move
            if self.thread and self.thread.is_alive():
                self.thread.join()
            # redo both computer and user move
            self.redo_once()
            self.redo_once()
        else:
            return
        self._black_score, self._white_score = get_score(self._board)
        self.update_game_state_signal.emit(self._board, self._turn, (self._black_score, self._white_score))
        self.update_available_moves_signal.emit([])
        self._next_move()

    def game_over(self):
        if self._black_score > self._white_score:
            winner = BLACK
        elif self._white_score > self._black_score:
            winner = WHITE
        else:
            winner = EMPTY
        self.game_over_signal.emit(winner)
