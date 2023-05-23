import time, random
from game.util import get_possible_moves

class HardStrategy(object):
    def get_move(self, board: list[list[int]], turn: int) -> tuple[int,int]:
        time.sleep(3)
        return random.choice(get_possible_moves(board, turn))
