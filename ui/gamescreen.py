from PyQt5.QtWidgets import QWidget

class GameplayScreen(QWidget):

    def __init__(self, stacked_layout):
        super().__init__()
        self.stacked_layout = stacked_layout
        self.initUI()

    def initUI(self):
        pass
