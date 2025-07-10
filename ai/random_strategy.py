import random
from ai.strategy import Strategy
from game.util import get_possible_moves

class RandomStrategy(Strategy):
    def get_move(self, board: list[list[int]], turn: int) -> tuple[int,int]:
        return random.choice(get_possible_moves(board, turn))