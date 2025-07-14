#  Othello Master

Othello game built with Python and PyQT5.
Supports 2 players and 1 player vs AI mode.

## Requirements
<ul>
    <li>Python 3.6+</li>
    <li>PyQT5</li>
</ul>

```
pip3 install pyqt5
```

## How to run
Simply run the main.py file with Python 3.6+.
```
python3 main.py
```

## AI
Multiple AI strategies implemented.

### Random
Takes completely random moves. Useful for testing and as a reference player.

### Greedy
Always makes a move that captures the most pieces. A player stronger than random to validate stronger models.

### Minimax
Minimax algorithm with alpha-beta pruning and a custom heuristic.

### MCTS
Monte Carlo Tree Search with random rollouts.

## Screenshots
![start screen](https://raw.githubusercontent.com/Nikola352/OthelloMaster/assets/ss1.png)
![game mode](https://raw.githubusercontent.com/Nikola352/OthelloMaster/assets/ss2.png)
![game start](https://raw.githubusercontent.com/Nikola352/OthelloMaster/assets/ss3.png)
![gameplay](https://raw.githubusercontent.com/Nikola352/OthelloMaster/assets/ss4.png)
