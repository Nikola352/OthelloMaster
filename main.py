from PyQt5.QtWidgets import QApplication
import sys
from ui.mainwindow import MainWindow
from game.game_controller import GameController

def main():
    app = QApplication(sys.argv)

    game_controller = GameController()
    win = MainWindow(game_controller)

    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()