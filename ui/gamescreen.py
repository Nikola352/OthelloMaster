from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QResizeEvent, QPixmap, QFont, QPalette, QIcon
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from game.constants import BLACK, WHITE, EMPTY

class GameplayScreen(QWidget):

    board_square_selected_signal = pyqtSignal(int, int)
    undo_signal = pyqtSignal()
    redo_signal = pyqtSignal()
    resign_signal = pyqtSignal()

    def __init__(self, stacked_layout):
        super().__init__()
        self.stacked_layout = stacked_layout
        self.initUI()
        self.board = [[EMPTY]*8 for _ in range(8)]

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 10)
        self.layout.setAlignment(Qt.AlignHCenter)
        
        upper_tray = QWidget()
        upper_tray.setMaximumHeight(50)
        upper_tray_layout = QHBoxLayout()
        upper_tray_layout.setContentsMargins(0, 10, 0, 0)
        upper_tray_layout.setSpacing(10)
        upper_tray_layout.setAlignment(Qt.AlignCenter)
        upper_tray.setLayout(upper_tray_layout)

        font = QFont()
        font.setBold(True)
        font.setPointSize(20)
        font.setWeight(75)

        palette = QPalette()
        palette.setColor(QPalette.ButtonText, Qt.black)

        # Black count label
        self.black_count_img = QLabel(self)
        self.black_count_img.setPixmap(QPixmap("ui/assets/black.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.black_count_img.setStyleSheet("border: 1px solid white")
        upper_tray_layout.addWidget(self.black_count_img)
        self.black_count_label = QLabel(self)
        self.black_count_label.setFont(font)
        self.black_count_label.setPalette(palette)
        self.black_count_label.setText("0")
        upper_tray_layout.addWidget(self.black_count_label)
        
        # Undo button
        self.undo_button = QPushButton(self)
        self.undo_button.setIcon(QIcon(QPixmap("ui/assets/undo.png").scaled(35, 35, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        self.undo_button.setMinimumSize(35, 35)
        self.undo_button.setIconSize(self.undo_button.size())
        self.undo_button.clicked.connect(self.undo)
        upper_tray_layout.addWidget(self.undo_button)

        # Redo button
        self.redo_button = QPushButton(self)
        self.redo_button.setIcon(QIcon(QPixmap("ui/assets/redo.png").scaled(35, 35, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        self.redo_button.setMinimumSize(35, 35)
        self.redo_button.setIconSize(self.redo_button.size())
        self.redo_button.clicked.connect(self.redo)
        upper_tray_layout.addWidget(self.redo_button)

        # Resign button
        self.resign_button = QPushButton(self)
        self.resign_button.setIcon(QIcon(QPixmap("ui/assets/flag.png").scaled(35, 35, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        self.resign_button.setMinimumSize(35, 35)
        self.resign_button.setIconSize(self.resign_button.size())
        self.resign_button.clicked.connect(self.resign)
        upper_tray_layout.addWidget(self.resign_button)

        font = QFont()
        font.setBold(True)
        font.setPointSize(20)
        font.setWeight(75)

        palette = QPalette()
        palette.setColor(QPalette.ButtonText, Qt.white)

        # White count label
        self.white_count_img = QLabel(self)
        self.white_count_img.setPixmap(QPixmap("ui/assets/white.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        upper_tray_layout.addWidget(self.white_count_img)
        self.white_count_label = QLabel(self)
        self.white_count_label.setFont(font)
        self.white_count_label.setPalette(palette)
        self.white_count_label.setStyleSheet("color: white")
        self.white_count_label.setText("0")
        upper_tray_layout.addWidget(self.white_count_label)

        self.layout.addWidget(upper_tray)

        # Board
        self.board = QWidget()
        side_len = min(self.geometry().height() - 50, self.geometry().width())
        self.board.setMinimumSize(side_len, side_len)

        self.board_layout = QGridLayout()
        self.board_layout.setSpacing(1)
        self.board_layout.setContentsMargins(2, 2, 2, 2)
        for i in range(8):
            self.board_layout.setRowStretch(i, 0)
        self.board.setLayout(self.board_layout)
        self.board.setStyleSheet("background-color: rgb(20,30,20)")
        self.layout.addWidget(self.board)

        sqare_size = int(side_len)//8
        self.board_buttons = []
        self.pieces = []
        for i in range(8):
            button_row = []
            piece_row = []
            for j in range(8):
                button = QPushButton(self)
                if i > 1 and i < 6 and j > 1 and j < 6:
                    button.setStyleSheet("""
                    :enabled {background-color: rgb(0,230,90);}
                    :disabled {background-color: rgb(0,170,70); opacity: 1;}
                    """)
                else:
                    button.setStyleSheet("""
                    :enabled {background-color: rgb(0,230,90);}
                    :disabled {background-color: rgb(0,150,60); opacity: 1;}
                    """)
                button.setFixedSize(sqare_size, sqare_size)
                button.clicked.connect(lambda _, i=i, j=j: self.boardSquareSelected(i, j))
                button.setEnabled(False)

                piece = QLabel(button)
                piece.setAlignment(Qt.AlignCenter)
                piece.setFixedSize(sqare_size, sqare_size)
                self.board_layout.addWidget(button, i, j)
                button_row.append(button)
                piece_row.append(piece)

            self.board_buttons.append(button_row)
            self.pieces.append(piece_row)

        self.setLayout(self.layout)

    def resizeEvent(self, event: QResizeEvent):
        side_len = min(event.size().height() - 50, event.size().width())
        # self.board.setMinimumSize(side_len, side_len)
        sqare_size = int(side_len)//8 -2
        for i in range(8):
            for j in range(8):
                self.board_buttons[i][j].setFixedSize(sqare_size, sqare_size)
                self.pieces[i][j].setFixedSize(sqare_size, sqare_size)
                pixmap = QPixmap(("ui/assets/black.png" if self.board[i][j] == BLACK else "ui/assets/white.png")).scaled(
                    self.board_buttons[i][j].size(),
                    Qt.IgnoreAspectRatio,
                    Qt.SmoothTransformation
                )
                self.pieces[i][j].setPixmap(pixmap)

    def showStartScreen(self):
        self.stacked_layout.setCurrentIndex(0)

    def boardSquareSelected(self, i: int, j: int):
        self.board_square_selected_signal.emit(i, j)

    def updateBoard(self, board: list[list[int]]):
        self.board = board
        for i in range(8):
            for j in range(8):
                if board[i][j] == BLACK:
                    pixmap = QPixmap("ui/assets/black.png").scaled(
                        self.board_buttons[i][j].size(),
                        Qt.IgnoreAspectRatio,
                        Qt.SmoothTransformation
                    )
                    self.pieces[i][j].setPixmap(pixmap)
                    self.pieces[i][j].setVisible(True)
                    self.pieces[i][j].setStyleSheet("background-color: transparent;")
                elif board[i][j] == WHITE:
                    pixmap = QPixmap("ui/assets/white.png").scaled(
                        self.board_buttons[i][j].size(),
                        Qt.IgnoreAspectRatio,
                        Qt.SmoothTransformation
                    )
                    self.pieces[i][j].setPixmap(pixmap)
                    self.pieces[i][j].setVisible(True)
                    self.pieces[i][j].setStyleSheet("background-color: transparent;")
                else:  # board[i][j] == 0
                    self.pieces[i][j].setVisible(False)

    def updateTurn(self, turn: int):
        if turn == BLACK:
            self.black_count_img.setStyleSheet("border: 1px solid white")
            self.white_count_img.setStyleSheet("border: 0px solid white")
        elif turn == WHITE:
            self.black_count_img.setStyleSheet("border: 0px solid white")
            self.white_count_img.setStyleSheet("border: 1px solid white")

    def updateScore(self, score: tuple[int,int]):
        self.black_count_label.setText(str(score[0]))
        self.white_count_label.setText(str(score[1]))

    @pyqtSlot(list, int, tuple)
    def updateGameState(self, board: list[list[int]], turn: int, score: tuple[int,int]):
        self.updateBoard(board)
        self.updateTurn(turn)
        self.updateScore(score)

    @pyqtSlot(list)
    def updateAvailableMoves(self, moves: list[tuple[int,int]]):
        for row in self.board_buttons:
            for button in row:
                button.setEnabled(False)
        for move in moves:
            self.board_buttons[move[0]][move[1]].setEnabled(True)

    def undo(self):
        self.undo_signal.emit()

    def redo(self):
        self.redo_signal.emit()

    def resign(self):
        reply = QMessageBox.question(self, 'Resign', "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.stacked_layout.setCurrentIndex(0)

    @pyqtSlot()
    def moveSkipped(self):
        QMessageBox.information(self, "Move Skipped", "No moves available. Skipping turn.")

    @pyqtSlot(int)
    def gameOver(self, winner: int):
        if winner == BLACK:
            QMessageBox.information(self, "Game Over", "Black wins!")
        elif winner == WHITE:
            QMessageBox.information(self, "Game Over", "White wins!")
        else:
            QMessageBox.information(self, "Game Over", "Draw!")
        self.stacked_layout.setCurrentIndex(0)
