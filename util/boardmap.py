class BoardMap(object):
    """
    A wrapper for a dictionary that uses a board as a key.
    Symmetric boards are considered equal.
    """
    def __init__(self) -> None:
        self._board_map = {}

    def _rotate_board(self, board: list[list[int]]) -> list[list[int]]:
        return list(zip(*board[::-1]))
        
    def __getitem__(self, key: list[list[int]]) -> float:
        if tuple(map(tuple, key)) in self._board_map:
            return self._board_map[tuple(map(tuple, key))]
        rotated_board = self._rotate_board(key)
        if tuple(map(tuple, rotated_board)) in self._board_map:
            return self._board_map[tuple(map(tuple, rotated_board))]
        rotated_board = self._rotate_board(rotated_board)
        if tuple(map(tuple, rotated_board)) in self._board_map:
            return self._board_map[tuple(map(tuple, rotated_board))]
        rotated_board = self._rotate_board(rotated_board)
        return self._board_map[tuple(map(tuple, rotated_board))]
    
    def __setitem__(self, key: list[list[int]], value: float) -> None:
        self._board_map[tuple(map(tuple, key))] = value

    def __contains__(self, key: list[list[int]]) -> bool:
        if tuple(map(tuple, key)) in self._board_map:
            return True
        rotated_board = self._rotate_board(key)
        if tuple(map(tuple, rotated_board)) in self._board_map:
            return True
        rotated_board = self._rotate_board(rotated_board)
        if tuple(map(tuple, rotated_board)) in self._board_map:
            return True
        rotated_board = self._rotate_board(rotated_board)
        return tuple(map(tuple, rotated_board)) in self._board_map
    
    def __delitem__(self, key: list[list[int]]) -> None:
        if tuple(map(tuple, key)) in self._board_map:
            del self._board_map[tuple(map(tuple, key))]
        rotated_board = self._rotate_board(key)
        if tuple(map(tuple, rotated_board)) in self._board_map:
            del self._board_map[tuple(map(tuple, rotated_board))]
        rotated_board = self._rotate_board(rotated_board)
        if tuple(map(tuple, rotated_board)) in self._board_map:
            del self._board_map[tuple(map(tuple, rotated_board))]
        rotated_board = self._rotate_board(rotated_board)
        del self._board_map[tuple(map(tuple, rotated_board))]
    
    def __len__(self) -> int:
        return len(self._board_map)
