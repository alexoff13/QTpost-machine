from typing import Union

from time import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem

from widgets.tape import Tape


class MainList(QListWidget):
    DEFAULT_NAME = 'main'

    def __init__(self, tape: Tape, parent: any = None):
        super().__init__(parent)
        self.__tape = tape
        self.__main = QListWidgetItem()
        self.__state = Tape.get_empty_data()
        self.__saved_state = None
        self.__set_main()
        self.__set_list()
        self.__last_time_dragged = float()

    @property
    def last_time_dragged(self) -> float:
        return self.__last_time_dragged

    @property
    def main(self) -> QListWidgetItem:
        return self.__main

    @property
    def state(self) -> dict:
        return self.__state.copy()

    @state.setter
    def state(self, value: dict) -> None:
        self.__state = value.copy()

    @property
    def saved_state(self) -> Union[dict, None]:
        return self.__saved_state

    @saved_state.setter
    def saved_state(self, value: dict) -> None:
        self.__saved_state = value

    def startDrag(self, supported_actions: Union[QtCore.Qt.DropActions, QtCore.Qt.DropAction]) -> None:
        self.__last_time_dragged = time()
        super().startDrag(supported_actions)

    def __set_main(self):
        self.__main.setText(self.DEFAULT_NAME)

    def __set_list(self) -> None:
        self.setFixedHeight(20)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setAcceptDrops(False)
        self.addItem(self.__main)

    def set_from_file(self, file: dict) -> None:
        self.__state = file.copy()
        self.__saved_state = file.copy()

    def save_state(self, global_: bool = False) -> None:
        if global_:
            self.__saved_state = self.__tape.get_data()
        else:
            self.__state = self.__tape.get_data()

    def has_unsaved_data(self) -> bool:
        return self.__state is not None and Tape.is_unsaved_data(self.__state)
