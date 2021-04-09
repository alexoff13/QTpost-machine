from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QHBoxLayout, QLabel, QVBoxLayout


class Index(QLabel):

    def __init__(self, parent: QWidget, index: int, width: int, height: int) -> None:
        super().__init__(str(index), parent=parent)
        self.width = width
        self.height = height
        self.setFixedSize(self.width, self.height)
        self.setAlignment(Qt.AlignHCenter)

    def set_as_carriage(self) -> None:
        self.setStyleSheet("font-weight: 500; color: blue; font-size: 7pt;")

    def set_as_ordinary(self) -> None:
        self.setStyleSheet("font-weight: 300; font-size: 7pt;")


class Cell(QPushButton):
    __MARKED = 'V'
    __NOT_MARKED = ''

    def __init__(self, parent: QWidget, width: int, height: int, is_marked: bool = False) -> None:
        super().__init__(self.__MARKED if is_marked else self.__NOT_MARKED, parent=parent)
        self.width = width
        self.height = height
        self.is_marked = is_marked
        self.setFixedSize(self.width, self.height)
        self.clicked.connect(self.reverse_marking)

    def reverse_marking(self) -> None:
        self.is_marked = not self.is_marked
        self.setText(self.__MARKED if self.is_marked else self.__NOT_MARKED)

    def mark(self) -> None:
        self.is_marked = True
        self.setText(self.__MARKED)

    def unmark(self) -> None:
        self.is_marked = False
        self.setText(self.__NOT_MARKED)


class TapeElement(QWidget):
    WIDTH = 25
    INDEX_HEIGHT = 15
    CELL_HEIGHT = 35

    def __init__(self, parent: QWidget, index, is_carriage: bool = False, is_marked: bool = False) -> None:
        super().__init__(parent)
        self.box = QVBoxLayout(self)
        self.index = Index(parent, index, self.WIDTH, self.INDEX_HEIGHT)
        self.cell = Cell(parent, self.WIDTH, self.CELL_HEIGHT, is_marked)
        self.index.set_as_carriage() if is_carriage else self.index.set_as_ordinary()
        self.box.addWidget(self.index, 0)
        self.box.addWidget(self.cell, 0)
        self.box.setContentsMargins(0, 0, 0, 0)

    def set_as_carriage(self) -> None:
        self.index.set_as_carriage()

    def set_as_ordinary(self) -> None:
        self.index.set_as_ordinary()


class Direction(QPushButton):
    WIDTH = TapeElement.WIDTH
    HEIGHT = 60
    LEFT = '<'
    RIGHT = '>'

    def __init__(self, is_left: bool):
        super().__init__(self.LEFT if is_left else self.RIGHT)
        self.setFixedSize(self.WIDTH, self.HEIGHT)


class Tape(QGridLayout):

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.__parent = parent
        self.__last_width = 0
        self.__tape_elements = dict()
        self.setAlignment(Qt.AlignBottom)

        self.__left_direction = Direction(True)
        self.__left_direction.clicked.connect(self.go_left)
        self.__right_direction = Direction(False)
        self.__right_direction.clicked.connect(self.go_right)
        self.__directions_layout = QGridLayout()
        self.__directions_layout.addWidget(self.__left_direction, 0, 0, alignment=Qt.AlignLeft)
        self.__directions_layout.addWidget(self.__right_direction, 0, 1, alignment=Qt.AlignRight)

        self.__left_element = 0
        self.__right_element = 0
        self.__tape_elements_layout = QHBoxLayout()
        self.__tape_elements_layout.setSpacing(0)
        self.__tape_elements_layout.setAlignment(Qt.AlignHCenter)

        self.addLayout(self.__tape_elements_layout, 0, 0)
        self.addLayout(self.__directions_layout, 0, 0)

    def __add_tape_element(self, index: int, is_carriage: bool = False, is_marked: bool = False) -> None:
        self.__tape_elements[index] = TapeElement(self.__parent, index, is_carriage, is_marked)

    @property
    def tape_elements(self) -> dict:
        return self.__tape_elements

    def draw(self, max_width: int, carriage_index: int = 0) -> None:
        self.__left_element = carriage_index
        self.__right_element = carriage_index
        self.__add_tape_element(carriage_index, is_carriage=True)
        self.__tape_elements_layout.addWidget(self.__tape_elements[carriage_index])
        self.resize(max_width)

    @staticmethod
    def __on_cell_click(cell: Cell) -> None:
        cell.click()

    # если до этого не будет вызываться draw, то всё полетит к херам
    def set_from_file(self, file: dict) -> None:
        self.__clear()
        self.__last_width -= 1
        self.draw(self.__last_width + 1, file['carriage'])
        for index in file['marked_cells']:
            if index not in self.__tape_elements:
                self.__add_tape_element(index, is_marked=True)
            else:
                self.__tape_elements[index].cell.mark()

    def __raise_directions(self) -> None:
        self.__left_direction.raise_()
        self.__right_direction.raise_()

    # сдвинуть ленту влево
    def go_left(self) -> None:
        self.__tape_elements[self.get_carriage_index()].set_as_ordinary()
        self.__add_left_tape_element()
        self.__delete_right_tape_element()
        self.__tape_elements[self.get_carriage_index()].set_as_carriage()
        self.__parent.runner.complete_event = True

    # сдвинуть ленту вправо
    def go_right(self) -> None:
        self.__tape_elements[self.get_carriage_index()].set_as_ordinary()
        self.__delete_left_tape_element()
        self.__add_right_tape_element()
        self.__tape_elements[self.get_carriage_index()].set_as_carriage()
        self.__parent.runner.complete_event = True

    # узнать, на какой позиции стоит каретка
    def get_carriage_index(self) -> int:
        return (self.__left_element + self.__right_element) // 2

    # узнать состояние каретки
    def is_carriage_marked(self) -> bool:
        return self.__tape_elements[self.get_carriage_index()].cell.is_marked

    def mark_carriage(self) -> None:
        self.__tape_elements[self.get_carriage_index()].cell.mark()
        self.__parent.runner.complete_event = True

    def unmark_carriage(self) -> None:
        self.__tape_elements[self.get_carriage_index()].cell.unmark()
        self.__parent.runner.complete_event = True

    def __clear(self) -> None:
        for index in range(self.__left_element, self.__right_element + 1, 1):
            self.__tape_elements_layout.removeWidget(self.__tape_elements[index])
        self.__tape_elements.clear()

    def reset(self) -> None:
        # TODO ладно, сделаешь
        pass

    def __add_right_tape_element(self) -> None:
        self.__right_element += 1
        if self.__right_element not in self.__tape_elements:
            self.__add_tape_element(self.__right_element)
        self.__tape_elements_layout.addWidget(self.__tape_elements[self.__right_element])
        self.__raise_directions()

    def __add_left_tape_element(self) -> None:
        self.__left_element -= 1
        if self.__left_element not in self.__tape_elements:
            self.__add_tape_element(self.__left_element)
        self.__tape_elements_layout.insertWidget(0, self.__tape_elements[self.__left_element])
        self.__raise_directions()

    def __delete_right_tape_element(self) -> None:
        self.__tape_elements_layout.removeWidget(self.__tape_elements[self.__right_element])
        if self.__tape_elements[self.__right_element].cell.is_marked:
            self.__tape_elements[self.__right_element] = None
        else:
            self.__tape_elements.pop(self.__right_element)
        self.__right_element -= 1

    def __delete_left_tape_element(self) -> None:
        self.__tape_elements_layout.removeWidget(self.__tape_elements[self.__left_element])
        if self.__tape_elements[self.__left_element].cell.is_marked:
            self.__tape_elements[self.__left_element] = None
        else:
            self.__tape_elements.pop(self.__left_element)
        self.__left_element += 1

    def resize(self, current_width: int) -> None:
        tape_width = self.__tape_elements_layout.sizeHint().width()
        if current_width > self.__last_width:
            while current_width - 2 * TapeElement.WIDTH - 15 > tape_width:
                self.__add_left_tape_element()
                self.__add_right_tape_element()
                tape_width += 2 * TapeElement.WIDTH
        elif current_width < self.__last_width:
            while current_width <= 22 + tape_width:
                self.__delete_left_tape_element()
                self.__delete_right_tape_element()
                tape_width -= 2 * TapeElement.WIDTH
        self.__last_width = current_width
