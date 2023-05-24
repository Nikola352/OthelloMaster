from game.constants import BLACK, WHITE, EMPTY
from game.util import get_score, get_possible_moves, calculate_board_position
from collections import deque

# Scaled sum of pieces on the board, based on their position.
def weight_sum_diff(board: list[list[int]]) -> int:
    weights = [
        [200 , -100, 100,  50,  50, 100, -100,  200],
        [-100, -200, -50, -50, -50, -50, -200, -100],
        [100 ,  -50, 100,   0,   0, 100,  -50,  100],
        [50  ,  -50,   0,   0,   0,   0,  -50,   50],
        [50  ,  -50,   0,   0,   0,   0,  -50,   50],
        [100 ,  -50, 100,   0,   0, 100,  -50,  100],
        [-100, -200, -50, -50, -50, -50, -200, -100],
        [200 , -100, 100,  50,  50, 100, -100,  200]
    ]
    if board[0][0] != EMPTY:
        weights[0][1] = 0
        weights[1][0] = 0
        weights[1][1] = 0
    if board[0][7] != EMPTY:
        weights[0][6] = 0
        weights[1][6] = 0
        weights[1][7] = 0
    if board[7][0] != EMPTY:
        weights[6][0] = 0
        weights[6][1] = 0
        weights[7][1] = 0
    if board[7][7] != EMPTY:
        weights[6][6] = 0
        weights[6][7] = 0
        weights[7][6] = 0
    black_val, white_val = 0, 0
    for row, val_row in zip(board, weights):
        for piece, value in zip(row, val_row):
            if piece == BLACK:
                black_val += value
            elif piece == WHITE:
                white_val += value
    if black_val + white_val == 0:
        return 0
    return (black_val - white_val) / (black_val + white_val)


# Relative difference of number of pieces
def num_pieces_diff(board: list[list[int]],) -> float:
    black_score, white_score = get_score(board)
    return (black_score - white_score) / (black_score + white_score)


# Relative difference of number of possible moves
def mobility_diff(board: list[list[int]]) -> float:
    black_moves = len(get_possible_moves(board, BLACK))
    white_moves = len(get_possible_moves(board, WHITE))
    if black_moves + white_moves == 0:
        raise ValueError("No moves left")
    return (black_moves - white_moves) / (black_moves + white_moves)


# True if adjacent to a stable piece in every direction
def stable_in_dir(i: int, j: int, is_stable: list[list[bool]]) -> True:
    if (i > 0 and not is_stable[i-1][j]) or (i < 7 and not is_stable[i+1][j]):
        return False
    if (j > 0 and not is_stable[i][j-1]) or (j < 7 and not is_stable[i][j+1]):
        return False
    if (i > 0 and j > 0 and not is_stable[i-1][j-1]) or (i < 7 and j < 7 and not is_stable[i+1][j+1]):
        return False
    if (i > 0 and j < 7 and not is_stable[i-1][j+1]) or (i < 7 and j > 0 and not is_stable[i+1][j-1]):
        return False
    return True

# Value based on total piece stability
def get_stability(board: list[list[int]], player: WHITE | BLACK) -> int:
    # stable pieces can never be flipped
    is_stable = [[False] * 8 for _ in range(8)]

    q = deque()
    # corners are always stable
    if board[0][0] == player:
        is_stable[0][0] = True
        q.append((0,0))
    if board[0][7] == player:
        is_stable[0][7] = True
        q.append((0,7))
    if board[7][0] == player:
        is_stable[7][0] = True
        q.append((7,0))
    if board[7][7] == player:
        is_stable[7][7] = True
        q.append((7,7))

    # bfs for stable pieces (considered stable if adjacent to a stable piece in all 4 directions)
    # note: piece can become stable due to opponent player's stable piece postitions, but that is not considered here
    while q:
        i, j = q.popleft()
        for delta_row, delta_col in [(0,1), (1,0), (0,-1), (-1,0)]:
            r = i + delta_row
            c = j + delta_col
            if r < 0 or r >= 8 or c < 0 or c >= 8:
                continue
            if board[r][c] != player or is_stable[r][c]:
                continue
            if stable_in_dir(r, c, is_stable):
                is_stable[r][c] = True
                q.append((r,c))

    # unstable pieces can be flipped in next move
    is_unstable = [[False] * 8 for _ in range(8)]
    moves = get_possible_moves(board, -player)
    for move in moves:
        new_board = calculate_board_position(board, -player, move)
        for i in range(8):
            for j in range(8):
                if board[i][j] == player and new_board[i][j] == -player:
                    is_unstable[i][j] = True

    # semistable pieces are those that are not stable nor unstable
    stable, semistable, unstable = 0, 0, 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == player:
                if is_stable[i][j]:
                    stable += 1
                elif is_unstable[i][j]:
                    unstable += 1
                else:
                    semistable += 1
    
    # arbitrary coefficients
    return 2 * stable + semistable - unstable

# Relative difference in piece stability 
def stability_diff(board: list[list[int]]) -> float:
    black_stability =  get_stability(board, BLACK)
    white_stability = get_stability(board, WHITE)
    if black_stability + white_stability == 0:
        return 0
    return (black_stability - white_stability) / (black_stability + white_stability)


# Relative difference in corner pieces
def corner_diff(board: list[list[int]]) -> float:
    black_corners, white_corners = 0, 0
    black_adjacent, white_adjacent = 0, 0

    if board[0][0] == BLACK:
        black_corners += 1
    elif board[0][0] == WHITE:
        white_corners += 1
    else:
        if board[0][1] == BLACK:
            black_adjacent += 1
        elif board[0][1] == WHITE:
            white_adjacent += 1
        if board[1][0] == BLACK:
            black_adjacent += 1
        elif board[1][0] == WHITE:
            white_adjacent += 1
        if board[1][1] == BLACK:
            black_adjacent += 1
        elif board[1][1] == WHITE:
            white_adjacent += 1

    if board[0][7] == BLACK:
        black_corners += 1
    elif board[0][7] == WHITE:
        white_corners += 1
    else:
        if board[0][6] == BLACK:
            black_adjacent += 1
        elif board[0][6] == WHITE:
            white_adjacent += 1
        if board[1][7] == BLACK:
            black_adjacent += 1
        elif board[1][7] == WHITE:
            white_adjacent += 1
        if board[1][6] == BLACK:
            black_adjacent += 1
        elif board[1][6] == WHITE:
            white_adjacent += 1

    if board[7][0] == BLACK:
        black_corners += 1
    elif board[7][0] == WHITE:
        white_corners += 1
    else:
        if board[7][1] == BLACK:
            black_adjacent += 1
        elif board[7][1] == WHITE:
            white_adjacent += 1
        if board[6][0] == BLACK:
            black_adjacent += 1
        elif board[6][0] == WHITE:
            white_adjacent += 1
        if board[6][1] == BLACK:
            black_adjacent += 1
        elif board[6][1] == WHITE:
            white_adjacent += 1

    if board[7][7] == BLACK:
        black_corners += 1
    elif board[7][7] == WHITE:
        white_corners += 1
    else:
        if board[7][6] == BLACK:
            black_adjacent += 1
        elif board[7][6] == WHITE:
            white_adjacent += 1
        if board[6][7] == BLACK:
            black_adjacent += 1
        elif board[6][7] == WHITE:
            white_adjacent += 1
        if board[6][6] == BLACK:
            black_adjacent += 1
        elif board[6][6] == WHITE:
            white_adjacent += 1

    if black_corners + white_corners == 0:
        corners = 0
    else:
        corners = (black_corners - white_corners) / (black_corners + white_corners)

    if black_adjacent + white_adjacent == 0:
        adjacent = 0
    else:
        adjacent = (black_adjacent - white_adjacent) / (black_adjacent + white_adjacent)

    return 3 * corners - adjacent


def evaluate_board(board: list[list[int]]) -> float:
    """
    Calculates static evaluation of the board.
    Higher values are better for black, and lower values are better for white.
    """
    num_pieces = num_pieces_diff(board)
    try:
        mobility = mobility_diff(board)
    except ValueError:
        if num_pieces > 0:
            return float("inf")
        else:
            return float("-inf")
    stability = stability_diff(board)
    corners = corner_diff(board)
    weighted_sum = weight_sum_diff(board)
    return 200*num_pieces + 30*mobility + 300*stability + 10000*corners + 400*weighted_sum
