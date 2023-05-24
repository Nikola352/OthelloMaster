from game.util import get_possible_moves, calculate_board_position
from ai.board_evaluation import evaluate_board

class MediumStrategy(object):
    def get_move(self, board: list[list[int]], turn: int) -> tuple[int,int]:
        moves = get_possible_moves(board, turn)
        best_move = moves[0]
        best_evaluation = turn * evaluate_board(calculate_board_position(board, turn, best_move))
        for move in moves[1:]:
            current_evaluation = turn * evaluate_board(calculate_board_position(board, turn, move))
            if current_evaluation > best_evaluation:
                best_move = move
                best_evaluation = current_evaluation
        return best_move