from time import sleep

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPalette, QIcon
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QLabel, QVBoxLayout, QGridLayout

from utils.signals import TapeSignals


class Index(QLabel):

    def __init__(self, index: int, width: int, height: int, is_carriage: bool = False, parent: any = None) -> None:
        super().__init__(str(index), parent=parent)
        self.__is_carriage = is_carriage
        self.set_as_carriage() if is_carriage else self.set_as_ordinary()
        self.setFixedSize(width, height)
        self.setAlignment(Qt.AlignHCenter)

    def is_carriage(self) -> bool:
        return self.__is_carriage

    def set_as_carriage(self) -> None:
        self.setStyleSheet("font-weight: 500; font-size: 7pt;")

    def set_as_ordinary(self) -> None:
        self.setStyleSheet("font-weight: 300; font-size: 7pt;")


class Cell(QPushButton):
    __MARKED = 'V'
    __NOT_MARKED = ''

    def __init__(self, width: int, height: int, is_marked: bool = False, parent: any = None) -> None:
        super().__init__(self.__MARKED if is_marked else self.__NOT_MARKED, parent=parent)
        self.__is_marked = is_marked
        self.setFixedSize(width, height)
        self.clicked.connect(self.reverse_marking)

    def is_marked(self) -> bool:
        return self.__is_marked

    def reverse_marking(self) -> None:
        self.__is_marked = not self.__is_marked
        self.setText(self.__MARKED if self.__is_marked else self.__NOT_MARKED)

    def mark(self) -> None:
        self.__is_marked = True
        self.setText(self.__MARKED)

    def unmark(self) -> None:
        self.__is_marked = False
        self.setText(self.__NOT_MARKED)

    def set_as_carriage(self) -> None:
        self.setStyleSheet('font-weight: 500; border: 1px solid;')

    def set_as_ordinary(self) -> None:
        self.setStyleSheet('font-weight: 300;')


class TapeElement(QWidget):
    WIDTH = 25
    INDEX_HEIGHT = 15
    CELL_HEIGHT = 35

    def __init__(self, index, is_carriage: bool = False, is_marked: bool = False, parent: any = None) -> None:
        super().__init__(parent)
        self.__index = Index(index, self.WIDTH, self.INDEX_HEIGHT, parent=parent)
        self.__cell = Cell(self.WIDTH, self.CELL_HEIGHT, is_marked, parent)
        if is_carriage:
            self.set_as_carriage()
        self.__element = QVBoxLayout(self)
        self.__element.setSpacing(0)
        self.__element.addWidget(self.__index, 0)
        self.__element.addWidget(self.__cell, 0)
        self.__element.setAlignment(Qt.AlignCenter)
        self.__element.setContentsMargins(0, 0, 0, 0)

    def is_carriage(self) -> bool:
        return self.__index.is_carriage()

    def set_as_carriage(self) -> None:
        self.__index.set_as_carriage()
        self.__cell.set_as_carriage()

    def set_as_ordinary(self) -> None:
        self.__index.set_as_ordinary()
        self.__cell.set_as_ordinary()

    def is_marked(self) -> bool:
        return self.__cell.is_marked()

    def reverse_marking(self) -> None:
        self.__cell.reverse_marking()

    def mark(self) -> None:
        self.__cell.mark()

    def unmark(self) -> None:
        self.__cell.unmark()


class Direction(QPushButton):
    WIDTH = 30
    HEIGHT = 65
    LEFT = 'icons/left.png'
    RIGHT = 'icons/right.png'

    def __init__(self, is_left: bool, parent: any = None):
        super().__init__(parent=parent)
        self.setIcon(QIcon(self.LEFT if is_left else self.RIGHT))
        self.setFixedSize(self.WIDTH, self.HEIGHT)


class Scrolling(QThread):
    def __init__(self, left: Direction, right: Direction, left_signal: QtCore.pyqtBoundSignal,
                 right_signal: QtCore.pyqtBoundSignal, is_left: bool = None) -> None:
        super().__init__()
        self.__left = left
        self.__right = right
        self.__left_signal = left_signal
        self.__right_signal = right_signal
        self.__mode = is_left  # left: True | right: False

    @staticmethod
    def pause(sec: float, button: Direction) -> None:
        k = 0
        while k < sec and button.isDown():
            sleep(0.05)
            k += 0.05

    def set_mode(self, is_left: bool):
        self.__mode = is_left

    def run(self) -> None:
        k = 0
        button = self.__left if self.__mode else self.__right
        signal = self.__left_signal if self.__mode else self.__right_signal
        while button.isDown():
            signal.emit()
            k += 1
            self.pause(0.05 if k > 2 else 0.2, button)


class Tape(QWidget):
    __signals = TapeSignals()

    def __init__(self, current_width: int, parent: any = None) -> None:
        super().__init__(parent=parent)
        self.__parent = parent
        self.__last_width = current_width - 1
        self.__tape_elements = dict()

        self.__left_direction = Direction(True)
        self.__left_direction.pressed.connect(self.__pressed_go_left)
        self.__right_direction = Direction(False)
        self.__right_direction.pressed.connect(self.__pressed_go_right)
        self.__directions_layout = QHBoxLayout()
        self.__directions_layout.addWidget(self.__left_direction, 0, alignment=Qt.AlignLeft)
        self.__directions_layout.addWidget(self.__right_direction, 1, alignment=Qt.AlignRight)

        self.__left_element = 0
        self.__right_element = 0
        self.__tape_elements_layout = QHBoxLayout()
        self.__tape_elements_layout.setSpacing(0)

        self.__main_layout = QGridLayout(self)
        self.__main_layout.addLayout(self.__tape_elements_layout, 0, 0, alignment=Qt.AlignHCenter)
        self.__main_layout.addLayout(self.__directions_layout, 0, 0)

        tape_background = QPalette()
        tape_background.setColor(QPalette.Background, Qt.color0)
        self.setAutoFillBackground(True)
        self.setPalette(tape_background)
        self.setFixedHeight(85)
        self.setLayout(self.__main_layout)

        self.__signals.to_left.connect(self.go_left)
        self.__signals.to_right.connect(self.go_right)
        self.__scrolling = Scrolling(self.__left_direction, self.__right_direction, self.__signals.to_left,
                                     self.__signals.to_right)

        self.draw(current_width)

    def __add_tape_element(self, index: int, is_carriage: bool = False, is_marked: bool = False) -> None:
        self.__tape_elements[index] = TapeElement(index, is_carriage, is_marked, self)

    @property
    def tape_elements(self) -> dict:
        return self.__tape_elements

    def draw(self, max_width: int, carriage_index: int = 0) -> None:
        self.__left_element = carriage_index
        self.__right_element = carriage_index
        self.__add_tape_element(carriage_index, is_carriage=True)
        self.__tape_elements_layout.addWidget(self.__tape_elements[carriage_index])
        self.resize_width(max_width)

    # если до этого не будет вызываться draw, то всё полетит к херам
    def set_from_file(self, file: dict) -> None:
        # полностью очистит элементы ленты и очистит self.__tape_elements
        self.__clear()
        self.__last_width -= 1
        # отрисует все элементы ленты и заполнит self.__tape_elements
        self.draw(self.__last_width + 1, file['carriage'])
        for index in file['marked_cells']:
            if index not in self.__tape_elements:
                self.__tape_elements[index] = None
            else:
                self.__tape_elements[index].mark()

    def __raise_directions(self) -> None:
        self.__left_direction.raise_()
        self.__right_direction.raise_()

    @staticmethod
    def __return_signal(callback: QtCore.pyqtBoundSignal) -> None:
        if type(callback) is QtCore.pyqtBoundSignal:
            callback.emit()

    def __pressed_go_left(self) -> None:
        self.__scrolling.set_mode(True)
        self.__scrolling.start()

    def __pressed_go_right(self) -> None:
        self.__scrolling.set_mode(False)
        self.__scrolling.start()

    # сдвинуть ленту влево
    def go_left(self, callback: QtCore.pyqtBoundSignal = None) -> None:
        self.__tape_elements[self.get_carriage_index()].set_as_ordinary()
        self.__add_left_tape_element()
        self.__delete_right_tape_element()
        self.__tape_elements[self.get_carriage_index()].set_as_carriage()
        self.__return_signal(callback)

    # сдвинуть ленту вправо
    def go_right(self, callback: QtCore.pyqtBoundSignal = None) -> None:
        self.__tape_elements[self.get_carriage_index()].set_as_ordinary()
        self.__delete_left_tape_element()
        self.__add_right_tape_element()
        self.__tape_elements[self.get_carriage_index()].set_as_carriage()
        self.__return_signal(callback)

    # узнать, на какой позиции стоит каретка
    def get_carriage_index(self) -> int:
        return (self.__left_element + self.__right_element) // 2

    # узнать состояние каретки
    def is_carriage_marked(self) -> bool:
        return self.__tape_elements[self.get_carriage_index()].is_marked()

    def mark_carriage(self, callback: QtCore.pyqtBoundSignal = None) -> None:
        self.__tape_elements[self.get_carriage_index()].mark()
        self.__return_signal(callback)

    def unmark_carriage(self, callback: QtCore.pyqtBoundSignal = None) -> None:
        self.__tape_elements[self.get_carriage_index()].unmark()
        self.__return_signal(callback)

    def __clear(self) -> None:
        for index in range(self.__left_element, self.__right_element + 1, 1):
            self.__tape_elements_layout.removeWidget(self.__tape_elements[index])
        self.__tape_elements.clear()

    def reset(self) -> None:
        reset_tape = {
            "carriage": 0,
            "marked_cells": []
        }
        self.set_from_file(reset_tape)

    def __add_right_tape_element(self) -> None:
        self.__right_element += 1
        self.__add_tape_element(self.__right_element, is_marked=self.__right_element in self.__tape_elements)
        self.__tape_elements_layout.addWidget(self.__tape_elements[self.__right_element])
        self.__raise_directions()

    def __add_left_tape_element(self) -> None:
        self.__left_element -= 1
        self.__add_tape_element(self.__left_element, is_marked=self.__left_element in self.__tape_elements)
        self.__tape_elements_layout.insertWidget(0, self.__tape_elements[self.__left_element])
        self.__raise_directions()

    def __delete_right_tape_element(self) -> None:
        self.__tape_elements_layout.removeWidget(self.__tape_elements[self.__right_element])
        try:
            if self.__tape_elements[self.__right_element].is_marked():
                self.__tape_elements[self.__right_element] = None
            else:
                self.__tape_elements.pop(self.__right_element)
        except AttributeError:
            pass
        self.__right_element -= 1

    def __delete_left_tape_element(self) -> None:
        self.__tape_elements_layout.removeWidget(self.__tape_elements[self.__left_element])
        try:
            if self.__tape_elements[self.__left_element].is_marked():
                self.__tape_elements[self.__left_element] = None
            else:
                self.__tape_elements.pop(self.__left_element)
        except AttributeError:
            pass
        self.__left_element += 1

    def get_data(self):
        tape_data = dict(carriage=self.get_carriage_index(), marked_cells=list())
        for index in self.__tape_elements:
            if self.__tape_elements[index] is None or self.__tape_elements[index].is_marked():
                tape_data['marked_cells'].append(index)
        return tape_data

    def has_unsaved_data(self) -> bool:
        return self.get_carriage_index() != 0 or len(self.get_data()['marked_cells']) > 0

    @staticmethod
    def is_unsaved_data(data: dict) -> bool:
        return data['carriage'] != 0 or len(data['marked_cells']) > 0

    @staticmethod
    def get_empty_data() -> dict:
        data = dict()
        data['carriage'] = 0
        data['marked_cells'] = list()
        return data

    def resize_width(self, current_width: int) -> None:
        tape_width = self.__tape_elements_layout.sizeHint().width()
        tape_width = TapeElement.WIDTH if tape_width == 0 else tape_width  # TODO: исправить этот натуральный костыль
        if current_width > self.__last_width:
            while current_width > tape_width + 4 * TapeElement.WIDTH - 10:
                self.__add_left_tape_element()
                self.__add_right_tape_element()
                tape_width += 2 * TapeElement.WIDTH
        elif current_width < self.__last_width:
            while current_width < tape_width + 2 * TapeElement.WIDTH - 10:
                self.__delete_left_tape_element()
                self.__delete_right_tape_element()
                tape_width -= 2 * TapeElement.WIDTH
        self.__last_width = current_width
