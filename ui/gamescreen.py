from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QResizeEvent, QPixmap, QFont, QPalette, QIcon
from PyQt5.QtCore import Qt, pyqtSignal

class GameplayScreen(QWidget):

    boardSquareSelectedSignal = pyqtSignal(int, int)
    undoSignal = pyqtSignal()
    redoSignal = pyqtSignal()

    def __init__(self, stacked_layout):
        super().__init__()
        self.stacked_layout = stacked_layout
        self.initUI()
        self.board = [[0]*8]*8

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
                    button.setStyleSheet("background-color: rgb(0,170,70)")
                else:
                    button.setStyleSheet("background-color: rgb(0,150,60)")
                button.setFixedSize(sqare_size, sqare_size)
                button.clicked.connect(lambda _, i=i, j=j: self.boardSquareSelected(i, j))

                piece = QLabel(button)
                piece.setAlignment(Qt.AlignCenter)
                piece.setFixedSize(sqare_size, sqare_size)
                piece.setPixmap(QPixmap("ui/assets/black.png").scaled(sqare_size, sqare_size,
                                                                      Qt.KeepAspectRatio,
                                                                      Qt.SmoothTransformation))
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
                pixmap = QPixmap(("ui/assets/black.png" if self.board[i][j] == 1 else "ui/assets/white.png")).scaled(
                    self.board_buttons[i][j].size(),
                    Qt.IgnoreAspectRatio,
                    Qt.SmoothTransformation
                )
                self.pieces[i][j].setPixmap(pixmap)

    def showStartScreen(self):
        self.stacked_layout.setCurrentIndex(0)

    def boardSquareSelected(self, i, j):
        self.boardSquareSelectedSignal.emit(i, j)

    def updateBoard(self, board):
        self.board = board
        for i in range(8):
            for j in range(8):
                if board[i][j] == 1:
                    pixmap = QPixmap("ui/assets/black.png").scaled(
                        self.board_buttons[i][j].size(),
                        Qt.IgnoreAspectRatio,
                        Qt.SmoothTransformation
                    )
                    self.pieces[i][j].setPixmap(pixmap)
                    self.pieces[i][j].setVisible(True)
                    self.pieces[i][j].setStyleSheet("background-color: transparent;")
                    self.board_buttons[i][j].setDisabled(True)
                elif board[i][j] == -1:
                    pixmap = QPixmap("ui/assets/white.png").scaled(
                        self.board_buttons[i][j].size(),
                        Qt.IgnoreAspectRatio,
                        Qt.SmoothTransformation
                    )
                    self.pieces[i][j].setPixmap(pixmap)
                    self.pieces[i][j].setVisible(True)
                    self.pieces[i][j].setStyleSheet("background-color: transparent;")
                    self.board_buttons[i][j].setDisabled(True)
                else:  # board[i][j] == 0
                    self.pieces[i][j].setVisible(False)
                    self.board_buttons[i][j].setDisabled(False)

    def updateTurn(self, turn):
        if turn == 1:
            self.black_count_img.setStyleSheet("border: 1px solid white")
            self.white_count_img.setStyleSheet("border: 0px solid white")
        else:
            self.black_count_img.setStyleSheet("border: 0px solid white")
            self.white_count_img.setStyleSheet("border: 1px solid white")

    def updateScore(self, score):
        self.black_count_label.setText(str(score[0]))
        self.white_count_label.setText(str(score[1]))

    def undo(self):
        self.undoSignal.emit()

    def redo(self):
        self.redoSignal.emit()

    def resign(self):
        print("resign")
