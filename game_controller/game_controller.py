from PyQt5.QtCore import QObject, pyqtSignal

class GameController(QObject):

    updateBoardSignal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.board = []

    def setInitialBoard(self):
        self.board = [] # 8x8 matrix: 0 = empty, 1 = black, -1 = white
        for i in range(8):
            self.board.append([])
            for j in range(8):
                self.board[i].append(0)
        self.board[3][3] = -1
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = -1

    def boardSquareSelected(self, i, j):
        self.board[i][j] = 1
        self.updateBoardSignal.emit(self.board)

    def startGame(self, mode, player_color, difficulty):
        print(mode, player_color, difficulty)
        self.setInitialBoard()
        self.updateBoardSignal.emit(self.board)