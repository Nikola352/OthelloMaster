from abc import abstractmethod
from ai.strategy import Strategy
from game.constants import BLACK, WHITE
from game.util import get_possible_moves
from util.boardmap import BoardMap

class TreeSearchStrategy(Strategy):
    def __init__(self):
        self._cahched_moves = {
            BLACK: BoardMap(unique=True),
            WHITE: BoardMap(unique=True)
        }

    def get_possible_moves(self, board: list[list[int]], turn: int) -> list[tuple[int,int]]:
        if board in self._cahched_moves[turn]:
            return self._cahched_moves[turn][board]
        moves = get_possible_moves(board, turn)
        self._cahched_moves[turn][board] = moves
        return moves
    
    @abstractmethod
    def get_move(self, board: list[list[int]], turn: int) -> tuple[int,int]:
        pass