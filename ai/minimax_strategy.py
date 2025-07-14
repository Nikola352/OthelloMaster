import time
from ai.tree_search_strategy import TreeSearchStrategy
from game.constants import BLACK, TIME_LIMIT, WHITE
from game.util import calculate_board_position, get_score
from ai.board_evaluation import evaluate_board
from util.boardmap import BoardMap

class MinimaxStrategy(TreeSearchStrategy):
    def __init__(self):
        super().__init__()
        self._cached_position = {
            BLACK: BoardMap(),
            WHITE: BoardMap()
        }
        self._cached_val = BoardMap()

    def get_move(self, board: list[list[int]], turn: int) -> tuple[int,int]:
        moves = self.get_possible_moves(board, turn)
        if len(moves) == 0:
            return None
        
        max_depth = 6
        self.start_time = time.time()
        best_move = None

        for depth in range(2, max_depth+1):
            if time.time() - self.start_time > TIME_LIMIT - 0.1:
                print(depth-1, time.time() - self.start_time)
                break
        
            self._cached_position[BLACK] = BoardMap()
            self._cached_position[WHITE] = BoardMap()

            if turn == BLACK:
                maxVal = float('-inf')
                for i, move in enumerate(moves[:]):
                    val = self.minimax(calculate_board_position(board, turn, move), -turn, depth, float('-inf'), float('inf'))
                    if val >= maxVal:
                        maxVal = val
                        best_move = move
                        moves[i], moves[0] = moves[0], moves[i] # best move is first for the next iterations
            else: # WHITE
                minVal = float('inf')
                for i, move in enumerate(moves[:]):
                    val = self.minimax(calculate_board_position(board, turn, move), -turn, depth, float('-inf'), float('inf'))
                    if val <= minVal:
                        minVal = val
                        best_move = move
                        moves[i], moves[0] = moves[0], moves[i]
        return best_move
    
    def minimax(self, board: list[list[int]], player: int, depth: int, alpha: float, beta: float) -> float:
        if board in self._cached_position[player]:
            return self._cached_position[player][board]

        if depth == 0 or time.time() - self.start_time > TIME_LIMIT - 0.05:
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
            self._cached_position[player][board] = maxVal
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
            self._cached_position[player][board] = minVal
            return minVal