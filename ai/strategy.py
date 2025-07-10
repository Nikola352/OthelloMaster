from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def get_move(self, board: list[list[int]], turn: int) -> tuple[int,int]:
        pass