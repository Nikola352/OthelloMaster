from concurrent.futures import Future, ProcessPoolExecutor
import copy
from math import sqrt, log
import random
import time
from ai.random_strategy import RandomStrategy
from ai.strategy import Strategy
from ai.tree_search_strategy import TreeSearchStrategy
from game.constants import BLACK, TIME_LIMIT
from game.util import calculate_board_position, get_score


C = sqrt(2)
GAMMA = 0.95
NUM_WORKERS = 8


class Node(object):
    def __init__(self, parent: "Node" = None, action: tuple | None = None):
        self.parent = parent
        self.action = action
        self.reward = 0
        self.visit_count = 0
        self.value_sum = 0
        self.children: list["Node"] = []

    @property
    def value(self) -> float:
        try:
            return self.value_sum / self.visit_count
        except ZeroDivisionError:
            return float("inf")

    @property
    def uct_score(self) -> float:
        try:
            return self.value_sum / self.visit_count + C * sqrt(log(self.parent.visit_count)/self.visit_count)
        except ZeroDivisionError:
            return float("inf")
        
    def best_child(self) -> "Node":
        return max(self.children, key=lambda n: n.uct_score)
    


class MonteCarloTreeSearchStrategy(TreeSearchStrategy):
    def __init__(self, gamma = GAMMA, num_workers = NUM_WORKERS):
        super().__init__()
        self._gamma = gamma
        self._num_workers = num_workers

    def get_move(self, board: list[list[int]], turn: int) -> tuple[int,int]:
        self._turn = turn
        self._board = board
        self._root = Node()
        self._root.visit_count = 1 # don't rollout from root

        start_time = time.time()

        with ProcessPoolExecutor(max_workers=self._num_workers) as executor:
            futures: list[tuple[Future[float], Node]] = []

            while time.time() - start_time < TIME_LIMIT - 0.5:
                node, board, turn = self.select_and_expand()

                # start a rollout in parallel
                future = executor.submit(self._parallel_rollout, board, turn)
                futures.append((future, node))

                # throttle the number of pending rollouts
                if len(futures) > self._num_workers * 2:
                    self._consume_futures(futures)

            self._consume_futures(futures)

        print(time.time() - start_time)

        return max(self._root.children, key=lambda n: n.value).action

    def select_and_expand(self) -> tuple[Node, list[list[int]], int]:
        node = self._root
        board = self._board
        turn = self._turn

        while node.children:
            node = node.best_child()
            if node.action is not None:
                board = calculate_board_position(board, turn, node.action)
            turn = -turn

        if node.visit_count == 0:
            return node, board, turn

        moves = self.get_possible_moves(board, turn)
        
        if not moves:
            if not self.get_possible_moves(board, -turn): # final state
                return node, board, turn
            # skip move
            node.children.append(Node(node, None))
            node = node.children[0]
            return node, board, -turn

        for move in moves:
            child = Node(node, move)
            node.children.append(child)

        return node.children[0], calculate_board_position(board, turn, moves[0]), -turn

    def rollout(self, board: list[list[int]], turn: int) -> float:
        while moves := self.get_possible_moves(board, turn) or self.get_possible_moves(board, -turn):
            if not moves:
                turn = -turn
                continue
            move = random.choice(moves)
            board = calculate_board_position(board, turn, move)
            turn = -turn
        return self._get_state_value(board, -turn) # get value for the player that played last

    def backpropagate(self, node: Node, reward: float):
        while node is not self._root:
            node.value_sum += reward
            node.visit_count += 1
            node = node.parent
            reward = -self._gamma * reward # reward for player is opposite of reward for opponent
        node.visit_count += 1

    def _parallel_rollout(self, board: list[list[int]], turn: int) -> float:
        return self.rollout(copy.deepcopy(board), turn)

    def _consume_futures(self, futures: list[tuple[Future[float], Node]]):
        for future, node in futures:
            reward = future.result()
            self.backpropagate(node, reward)
        futures.clear()

    def _get_state_value(self, board: list[list[int]], turn: int):
        black, white = get_score(board)
        if black == white:
            return 0
        player, opponent = (black, white) if turn == BLACK else (white, black)
        return 1 if player > opponent else -1
