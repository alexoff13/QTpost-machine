from PyQt5.QtWidgets import QPushButton, QWidget


class Numbering:
    pass


class Carriage:
    pass


class Cell:

    def __init__(self, button: QPushButton, is_marked: bool = False) -> None:
        self.button = button
        self.is_marked = is_marked


class Tape:

    __MARKED = '+'
    __NOT_MARKED = ''
    __LENGTH = 51

    def __init__(self, app: QWidget, x: int, y: int) -> None:
        self.__app = app
        self.__x = x
        self.__y = y
        self.__left = 0
        self.__right = self.__LENGTH
        self.__tape = dict()

    def __set_cell(self, i: int, x: int, y: int, marked: bool = False) -> None:
        text = self.__MARKED if marked else self.__NOT_MARKED
        self.__tape[i] = Cell(QPushButton(text, self.__app), marked)
        self.__tape[i].button.move(x, y)
        self.__tape[i].button.resize(15, 20)
        self.__tape[i].button.clicked.connect(lambda: self.__on_cell_click(self.__tape[i]))

    @property
    def cells(self) -> dict:
        return self.__tape

    def show(self) -> None:
        x = self.__x
        y = self.__y
        # установка кнопки "сместиться влево"
        self.__left = QPushButton('<', self.__app)
        self.__left.move(x, y)
        self.__left.resize(15, 20)
        # установка ячеек ленты
        for i in range(0, self.__LENGTH):
            x += 15
            self.__set_cell(i, x, y)
        # установка кнопки "сместиться право"
        self.__right = QPushButton('>', self.__app)
        self.__right.move(x + 15, y)
        self.__right.resize(15, 20)

    def __on_cell_click(self, cell: Cell) -> None:
        cell.button.setText(self.__NOT_MARKED if cell.is_marked else self.__MARKED)
        cell.is_marked = not cell.is_marked
