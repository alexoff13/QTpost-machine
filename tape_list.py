from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QColumnView, QPushButton, QVBoxLayout


class TapeList(QWidget):

    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.__parent = parent
        self.__buttons_layout = QHBoxLayout()
        self.__buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.__buttons_layout.setAlignment(Qt.AlignLeft)
        self.__buttons = QWidget()
        self.__buttons.setLayout(self.__buttons_layout)
        self.__buttons.setFixedHeight(25)
        self.__column = QColumnView()

        # TODO: привязять кнопки к функциям
        self.__add = QPushButton('Add')
        self.__remove = QPushButton('Remove')
        self.__clear = QPushButton('Clear')

        self.__main_layout = QVBoxLayout(self)
        self.__main_layout.addWidget(self.__buttons)
        self.__main_layout.addWidget(self.__column)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.__main_layout)

        self.draw()

    def draw(self) -> None:
        self.__add.setFixedWidth(50)
        self.__remove.setFixedWidth(50)
        self.__clear.setFixedWidth(50)

        self.__buttons_layout.addWidget(self.__add)
        self.__buttons_layout.addWidget(self.__remove)
        self.__buttons_layout.addWidget(self.__clear)