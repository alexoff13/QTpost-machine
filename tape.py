from PyQt5.QtCore import Qt
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


class Tape(QGridLayout):
    __MARKED = '+'
    __NOT_MARKED = ''

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.__parent = parent
        self.__last_width = 0
        self.__tape = dict()

        self.__left = Direction(True)
        self.__left.clicked.connect(self.go_left)
        self.__right = Direction(False)
        self.__right.clicked.connect(self.go_right)
        self.__directions = QGridLayout()
        self.__directions.addWidget(self.__left, 0, 0, alignment=Qt.AlignLeft)
        self.__directions.addWidget(self.__right, 0, 1, alignment=Qt.AlignRight)

        self.__left_cell = 0
        self.__right_cell = 0
        self.__cells = QHBoxLayout()
        self.__cells.setSpacing(0)
        self.__cells.setAlignment(Qt.AlignHCenter)

    def __add_cell(self, i: int, is_marked: bool = False) -> None:
        self.__tape[i] = Cell(is_marked)
        self.__tape[i].clicked.connect(lambda: self.__on_cell_click(self.__tape[i]))

    @property
    def cells(self) -> dict:
        return self.__tape

    def draw(self, max_width: int) -> None:
        self.__add_cell(0)
        self.__cells.addWidget(self.__tape[0])
        self.resize(max_width)
        self.addLayout(self.__cells, 0, 0)
        self.addLayout(self.__directions, 0, 0)
        self.__left.raise_()
        self.__right.raise_()

    @staticmethod
    def __on_cell_click(cell: Cell) -> None:
        cell.click()

    def set_from_file(self, file: list) -> None:
        for cell in file:
            if cell[0] not in self.__tape:
                self.__add_cell(cell[0], cell[1])
            elif self.__tape[cell[0]].is_marked != cell[1]:
                self.__on_cell_click(self.__tape[cell[0]])

    def __top_directions(self) -> None:
        self.__left.raise_()
        self.__right.raise_()

    # сдвинуть ленту влево
    def go_left(self) -> None:
        self.__add_left_cell()
        self.__delete_right_cell()

    # сдвинуть ленту вправо
    def go_right(self) -> None:
        self.__delete_left_cell()
        self.__add_right_cell()

    # узнать состояние каретки
    def is_carriage_marked(self) -> bool:
        return self.__tape[(self.__left_cell + self.__right_cell) // 2].is_marked

    # изверсировать состояние каретки
    def inverse_carriage(self) -> None:
        self.__tape[(self.__left_cell + self.__right_cell) // 2].click()

    def __add_right_cell(self) -> None:
        self.__right_cell += 1
        if self.__right_cell not in self.__tape:
            self.__add_cell(self.__right_cell)
        self.__cells.addWidget(self.__tape[self.__right_cell])
        self.__top_directions()

    def __add_left_cell(self) -> None:
        self.__left_cell -= 1
        if self.__left_cell not in self.__tape:
            self.__add_cell(self.__left_cell)
        self.__cells.insertWidget(0, self.__tape[self.__left_cell])
        self.__top_directions()

    def __delete_right_cell(self) -> None:
        if self.__tape[self.__right_cell].is_marked:
            self.__cells.removeWidget(self.__tape[self.__right_cell])
        else:
            self.__cells.removeWidget(self.__tape.pop(self.__right_cell))
        self.__right_cell -= 1

    def __delete_left_cell(self) -> None:
        if self.__tape[self.__left_cell].is_marked:
            self.__cells.removeWidget(self.__tape[self.__left_cell])
        else:
            self.__cells.removeWidget(self.__tape.pop(self.__left_cell))
        self.__left_cell += 1

    def resize(self, current_width: int) -> None:
        tape_width = self.__cells.sizeHint().width()
        if current_width > self.__last_width:
            while current_width - 2 * Cell.WIDTH - 15 > tape_width:
                self.__add_left_cell()
                self.__add_right_cell()
                tape_width += 2 * Cell.WIDTH
        elif current_width < self.__last_width:
            while current_width <= 22 + tape_width:
                self.__delete_left_cell()
                self.__delete_right_cell()
                tape_width -= 2 * Cell.WIDTH
        self.__last_width = current_width
