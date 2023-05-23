import random
from game.util import get_possible_moves

class EasyStrategy(object):
    def get_move(self, board: list[list[int]], turn: int) -> tuple[int,int]:
        return random.choice(get_possible_moves(board, turn))