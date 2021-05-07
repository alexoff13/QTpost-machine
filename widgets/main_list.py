from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem

from widgets.tape import Tape


class MainList(QListWidget):
    DEFAULT_NAME = 'main'

    def __init__(self, tape: Tape, parent: any = None):
        super().__init__(parent)
        self.__tape = tape
        self.__main = QListWidgetItem()
        self.__state = Tape.get_empty_data()
        self.__set_main()
        self.__set_list()

    def __set_main(self):
        self.__main.setText(self.DEFAULT_NAME)

    def __set_list(self) -> None:
        self.setFixedHeight(20)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setAcceptDrops(False)
        self.addItem(self.__main)

    @property
    def main(self) -> QListWidgetItem:
        return self.__main

    @property
    def state(self) -> dict:
        return self.__state.copy()

    @state.setter
    def state(self, value: dict) -> None:
        self.__state = value.copy()

    def save_state(self) -> None:
        self.__state = self.__tape.get_data()

    def has_unsaved_data(self) -> bool:
        return self.__state is not None and Tape.is_unsaved_data(self.__state)
