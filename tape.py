from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QHBoxLayout


class Numbering:
    pass


class Cell(QPushButton):
    WIDTH = 30
    HEIGHT = 40
    __MARKED = '+'
    __NOT_MARKED = ''

    def __init__(self, is_marked: bool = False) -> None:
        super().__init__(self.__MARKED if is_marked else self.__NOT_MARKED)
        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.is_marked = is_marked

    def click(self) -> None:
        self.is_marked = not self.is_marked
        self.setText(self.__MARKED if self.is_marked else self.__NOT_MARKED)


class Direction(QPushButton):
    WIDTH = Cell.WIDTH
    HEIGHT = 60
    LEFT = '<'
    RIGHT = '>'

    def __init__(self, is_left: bool):
        super().__init__(self.LEFT if is_left else self.RIGHT)
        self.setFixedSize(self.WIDTH, self.HEIGHT)


class Tape(QWidget):
    __MARKED = '+'
    __NOT_MARKED = ''

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.__parent = parent
        self.__last_width = 0
        self.__tape = dict()
        self.installEventFilter(self)
        self.__layout = QGridLayout(self)

        self.__cells = QHBoxLayout()
        self.__cells.setSpacing(0)
        self.__cells.setAlignment(Qt.AlignHCenter)

        self.__left = Direction(True)
        self.__right = Direction(False)
        self.__directions = QGridLayout()
        self.__directions.addWidget(self.__left, 0, 0, alignment=Qt.AlignLeft)
        self.__directions.addWidget(self.__right, 0, 1, alignment=Qt.AlignRight)

    def __set_cell(self, i: int, is_marked: bool = False) -> None:
        self.__tape[i] = Cell(is_marked)
        self.__tape[i].clicked.connect(lambda: self.__on_cell_click(self.__tape[i]))

    @property
    def cells(self) -> dict:
        return self.__tape

    # TODO должно работать под любой размер ширины окна (чтобы создавалось нечетное количество ячеек)
    def create_tape(self, max_width: int) -> None:
        self.__last_width = max_width

        current_width = self.__cells.sizeHint().width()
        i = -((max_width - 30) // Cell.WIDTH // 2)
        while current_width + Cell.WIDTH < max_width:
            self.__set_cell(i)
            self.__cells.addWidget(self.__tape[i])
            current_width += Cell.WIDTH
            i += 1

        self.__layout.addLayout(self.__cells, 0, 0)
        self.__layout.addLayout(self.__directions, 0, 0)
        self.__left.raise_()
        self.__right.raise_()

    @staticmethod
    def __on_cell_click(cell: Cell) -> None:
        cell.click()

    def set_from_file(self, file: list) -> None:
        for cell in file:
            if self.__tape[cell[0]].is_marked != cell[1]:
                self.__on_cell_click(self.__tape[cell[0]])

    def eventFilter(self, obj: QObject, event: QEvent):
        print('here')
        if event.type() == QtCore.QEvent.Resize:
            current_width = self.__parent.size().width()
            print(current_width)

            if current_width > self.__last_width:
                while current_width - 2 * Cell.WIDTH - 10 > self.__cells.sizeHint().width():
                    i = min(self.__tape.keys())
                    self.__set_cell(i)
                    self.__cells.insertWidget(0, self.__tape[i])
                    self.left.raise_()

                    i = max(self.__tape.keys())
                    self.__set_cell(i)
                    self.__cells.insertWidget(0, self.__tape[i])
                    self.left.raise_()
                    self.right.raise_()

            elif current_width < self.__last_width:
                while current_width <= 20 + self.__cells.sizeHint().width():
                    self.__cells.removeWidget(self.__tape.pop(min(self.__tape.keys())))
                    self.__cells.removeWidget(self.__tape.pop(max(self.__tape.keys())))

            self.__last_width = current_width

        return super().eventFilter(obj, event)
