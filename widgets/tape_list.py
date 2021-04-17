from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QColumnView, QPushButton, QVBoxLayout


class TapeList(QWidget):

    def __init__(self, parent: any = None):
        super().__init__(parent=parent)
        self.__parent = parent
        self.__button_width = 50
        self.__button_height = 25

        self.__add = QPushButton()
        self.__remove = QPushButton()
        self.__clear = QPushButton()
        self.__buttons = QWidget()
        self.__column = QColumnView()

        self.__buttons_layout = QHBoxLayout()
        self.__main_layout = QVBoxLayout()

        self.draw()

    def __set_add(self) -> None:
        self.__add.setText('Add')
        self.__add.setToolTip('')  # TODO: добавить
        self.__add.setFixedWidth(self.__button_width)
        # TODO: привязять к функции

    def __set_remove(self) -> None:
        self.__remove.setText('Remove')
        self.__remove.setToolTip('')  # TODO: добавить
        self.__remove.setFixedWidth(self.__button_width)
        # TODO: привязять к функции

    def __set_clear(self) -> None:
        self.__clear.setText('Clear')
        self.__clear.setToolTip('')  # TODO: добавить
        self.__clear.setFixedWidth(self.__button_width)
        # TODO: привязять к функции

    def __set_buttons_layout(self) -> None:
        self.__buttons_layout.addWidget(self.__add)
        self.__buttons_layout.addWidget(self.__remove)
        self.__buttons_layout.addWidget(self.__clear)
        self.__buttons_layout.setAlignment(Qt.AlignLeft)
        self.__buttons_layout.setContentsMargins(0, 0, 0, 0)

    def __set_buttons(self) -> None:
        self.__buttons.setLayout(self.__buttons_layout)
        self.__buttons.setFixedHeight(self.__button_height)

    def __set_column(self) -> None:
        # TODO: добавить настройки для столбца
        pass

    def __set_main_layout(self) -> None:
        self.__main_layout.addWidget(self.__buttons)
        self.__main_layout.addWidget(self.__column)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

    def draw(self) -> None:
        self.__set_add()
        self.__set_remove()
        self.__set_clear()
        self.__set_buttons_layout()
        self.__set_buttons()
        self.__set_column()
        self.__set_main_layout()
        self.setLayout(self.__main_layout)
