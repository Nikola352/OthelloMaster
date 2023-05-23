from copy import deepcopy
from game.constants import BLACK, WHITE

def check_dir(i, j, deltaRow, deltaCol, board, turn) -> set[tuple[int,int]]:
    moves = set()
    start = False; middle = False
    while i>=0 and i<8 and j>=0 and j<8:
        if board[i][j] == turn:
            start = True
            middle = False
        elif board[i][j] == -turn:
            if start:
                middle = True
        else:
            if middle:
                moves.add((i,j))
            start = False
            middle = False
        i += deltaRow
        j += deltaCol
    return moves


def get_possible_moves(board: list[list[int]], turn: int) -> list[tuple[int,int]]:
    moves = set()
    for i in range(8):
        moves.update(check_dir(i, 0, 0, 1, board, turn))
        moves.update(check_dir(0, i, 1, 0, board, turn))
        moves.update(check_dir(i, 0, 1, 1, board, turn))
        moves.update(check_dir(0, i, 1, 1, board, turn))
        moves.update(check_dir(0, i, 1, -1, board, turn))
        moves.update(check_dir(i, 7, 1, -1, board, turn))
        moves.update(check_dir(i, 7, 0, -1, board, turn))
        moves.update(check_dir(7, i, -1, 0, board, turn))
        moves.update(check_dir(i, 7, -1, -1, board, turn))
        moves.update(check_dir(7, i, -1, -1, board, turn))
        moves.update(check_dir(7, i, -1, 1, board, turn))
        moves.update(check_dir(i, 0, -1, 1, board, turn))
    return list(moves)


def calculate_board_position(board: list[list[int]], turn: int, move: tuple[int,int]) -> list[list[int]]:
    res_board = deepcopy(board)
    res_board[move[0]][move[1]] = turn
    dirs = ((0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1))
    for d in dirs:
        found_opp = False
        found_own = False
        i, j = move
        i += d[0]; j += d[1]
        while i>=0 and i<8 and j>=0 and j<8:
            if board[i][j] == turn:
                found_own = True
                break
            elif board[i][j] == -turn:
                found_opp = True
            else:
                break
            i += d[0]; j += d[1]
        if found_opp and found_own:
            i, j = move
            i += d[0]; j += d[1]
            while i>=0 and i<8 and j>=0 and j<8 and board[i][j] != turn:
                res_board[i][j] = turn
                i += d[0]; j += d[1]
    return res_board


def get_score(board: list[list[int]]) -> tuple[int, int]:
    black_score = 0
    white_score = 0
    for row in board:
        for cell in row:
            if cell == BLACK:
                black_score += 1
            elif cell == WHITE:
                white_score += 1
    return (black_score, white_score)
