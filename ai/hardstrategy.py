import time, random
from game.constants import BLACK, WHITE
from game.util import get_possible_moves, calculate_board_position, get_score
from ai.board_evaluation import evaluate_board
from util.boardmap import BoardMap

class HardStrategy(object):
    def __init__(self):
        self._cached_position = {
            BLACK: BoardMap(),
            WHITE: BoardMap()
        }
        self._cached_val = BoardMap()
        self._cahched_moves = {
            BLACK: BoardMap(),
            WHITE: BoardMap()
        }

    def get_possible_moves(self, board: list[list[int]], turn: int) -> list[tuple[int,int]]:
        if board in self._cahched_moves[turn]:
            return self._cahched_moves[turn][board]
        moves = get_possible_moves(board, turn)
        self._cahched_moves[turn][board] = moves
        return moves

    def get_move(self, board: list[list[int]], turn: int) -> tuple[int,int]:
        moves = self.get_possible_moves(board, turn)
        if len(moves) == 0:
            return None
        
        max_depth = 6
        self.start_time = time.time()
        best_move = None

        for depth in range(2, max_depth+1):
            if time.time() - self.start_time > 2.5:
                print(depth-1, time.time() - self.start_time)
                break
        
            self._cached_position[BLACK] = BoardMap()
            self._cached_position[WHITE] = BoardMap()

            if turn == BLACK:
                maxVal = float('-inf')
                for i, move in enumerate(moves[:]):
                    val = self.minimax(calculate_board_position(board, turn, move), turn, depth, float('-inf'), float('inf'))
                    if val >= maxVal:
                        maxVal = val
                        best_move = move
                        moves[i], moves[0] = moves[0], moves[i] # best move is first for the next iterations
            else: # WHITE
                minVal = float('inf')
                for i, move in enumerate(moves[:]):
                    val = self.minimax(calculate_board_position(board, turn, move), turn, depth, float('-inf'), float('inf'))
                    if val <= minVal:
                        minVal = val
                        best_move = move
                        moves[i], moves[0] = moves[0], moves[i]
            self._cahched_moves[turn][board] = moves
        return best_move
    
    def minimax(self, board: list[list[int]], player: int, depth: int, alpha: float, beta: float) -> float:
        if board in self._cached_position[player]:
            return self._cached_position[player][board]

        if depth == 0 or time.time() - self.start_time > 2.95:
            if board in self._cached_val:
                return self._cached_val[board]
            val = evaluate_board(board)
            self._cached_val[board] = val
            return val
        
        moves = self.get_possible_moves(board, player)
        if len(moves) == 0:
            if len(self.get_possible_moves(board, -player)) == 0: # game over state
                black_score, white_score = get_score(board)
                if black_score > white_score:
                    return float('inf')
                elif black_score < white_score:
                    return float('-inf')
                return 0
            # skip current player's move
            return self.minimax(board, -player, depth-1, alpha, beta)
        
        if player == BLACK: # max player
            maxVal = float('-inf')
            for i, move in enumerate(moves[:]):
                val = self.minimax(calculate_board_position(board, player, move), -player, depth-1, alpha, beta)
                if val >= maxVal:
                    maxVal = val
                    moves[i], moves[0] = moves[0], moves[i]
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            self._cached_position[player][tuple(map(tuple, board))] = maxVal
            return maxVal
        else: # WHITE: min player
            minVal = float('inf')
            for i, move in enumerate(moves[:]):
                val = self.minimax(calculate_board_position(board, player, move), -player, depth-1, alpha, beta)
                if val <= minVal:
                    minVal = val
                    moves[i], moves[0] = moves[0], moves[i]
                beta = min(beta, val)
                if beta <= alpha:
                    break
            self._cached_position[player][tuple(map(tuple, board))] = minVal
            return minVal