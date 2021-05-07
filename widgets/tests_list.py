from typing import Union

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem

from widgets.tape import Tape


class Data:
    test: QListWidgetItem
    state: dict


class TestsList(QListWidget):
    DEFAULT_NAME = 'test'

    def __init__(self, tape: Tape, parent: any = None):
        super().__init__(parent)
        self.__tape = tape
        self.__tests = dict()
        self.__set_list()

    def __set_list(self) -> None:
        # устанавливает возможность Drag'n'Drop элементов
        self.setDragDropMode(QAbstractItemView.DragDrop)
        # устанавливает возможность сразу нескольких элементов
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def get_test_name(self, name: str = DEFAULT_NAME, ignore_name: str = None, other: str = '') -> str:
        if not name:
            name = self.DEFAULT_NAME
        k = 1
        new_name = name
        while new_name in self.__tests and new_name != ignore_name or new_name == other:
            new_name = f'{name}-{k}'
            k += 1
        return new_name

    def add_test(self, test_name: str = None, state: dict = None, test: QListWidgetItem = None) -> QListWidgetItem:
        if test_name is None:
            test_name = self.get_test_name()
        if test is None:
            test = QListWidgetItem()
        test.setText(test_name)
        test.last_name = test_name
        test.setFlags(test.flags() | Qt.ItemIsEditable)
        self.addItem(test)
        self.__tape.reset()
        self.__tests[test_name] = Data()
        self.__tests[test_name].test = test
        self.__tests[test_name].state = state if state is not None else Tape.get_empty_data()
        return test

    def remove_test(self, test: QListWidgetItem) -> bool:
        try:
            self.takeItem(self.row(test))
            self.__tests.pop(test.text())
            return True
        except Exception:
            return False

    def get_last(self) -> Union[QListWidgetItem, None]:
        return self.item(self.count() - 1) if self.count() > 0 else None

    def get_state(self, test: QListWidgetItem) -> dict:
        return self.__tests[test.text()].state

    def clear(self) -> None:
        for test_name in self.__tests:
            self.takeItem(self.row(self.__tests[test_name].test))
        self.__tests.clear()

    def save_state(self, test: QListWidgetItem) -> None:
        if test.text() in self.__tests:
            self.__tests[test.text()].state = self.__tape.get_data()

    def get_data(self) -> dict:
        data = dict()
        for test_name in self.__tests:
            data[test_name] = self.__tests[test_name].state
        return data

    # TODO: возможно лучше предложить выбор: загрузка с заменой или с добавлением в конец
    def set_from_file(self, file: dict) -> None:
        self.clear()
        for test_name in file:
            self.add_test(test_name, file[test_name])

    def has_unsaved_data(self) -> bool:
        return len(self.__tests) > 0

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.MoveAction)
            event.accept()
            links = list()
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
        else:
            event.setDropAction(Qt.MoveAction)
            super().dropEvent(event)
