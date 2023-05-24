class BoardMap(object):
    """
    A wrapper for a dictionary that uses a board as a key.
    Symmetric boards are considered equal, unless unique is set to True.
    """
    def __init__(self, unique = False) -> None:
        self._board_map = {}
        self._unique = unique

    def _rotate_board(self, board: list[list[int]]) -> list[list[int]]:
        return list(zip(*board[::-1]))
        
    def __getitem__(self, key: list[list[int]]) -> float:
        if self._unique:
            return self._board_map[tuple(map(tuple, key))]
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
        if self._unique:
            return tuple(map(tuple, key)) in self._board_map
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
        if self._unique:
            del self._board_map[tuple(map(tuple, key))]
            return
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
