from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QListWidget, QListWidgetItem, \
    QAbstractItemView

from widgets.tape import Tape


class TapeList(QWidget):
    __DEFAULT_NAME = 'tape'

    def __init__(self, tape: Tape, parent: any = None):
        super().__init__(parent=parent)
        self.__tape = tape
        self.__parent = parent
        self.__button_width = 50
        self.__button_height = 25
        self.__tapes = dict()
        self.__active_tape = None
        
        self.__add = QPushButton()
        self.__remove = QPushButton()
        self.__clear = QPushButton()
        self.__buttons = QWidget()
        self.__list = QListWidget()

        self.__buttons_layout = QHBoxLayout()
        self.__main_layout = QVBoxLayout()

        self.__draw()

    def __set_add(self) -> None:
        self.__add.setText('Add')
        self.__add.setToolTip('')  # TODO: добавить
        self.__add.setFixedWidth(self.__button_width)
        self.__add.clicked.connect(self.__on_add_click)

    def __set_remove(self) -> None:
        self.__remove.setText('Remove')
        self.__remove.setToolTip('')  # TODO: добавить
        self.__remove.setFixedWidth(self.__button_width)
        self.__remove.clicked.connect(self.__on_remove_click)

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

    def __get_name(self) -> str:
        # такой странный геттер дефолтного названия, чтобы всегда создавался tape с наименьшим номером
        k = 1
        name = f'{self.__DEFAULT_NAME}{k}'
        while name in self.__tapes:
            k += 1
            name = f'{self.__DEFAULT_NAME}{k}'
        return name

    def __add_item(self) -> None:
        self.save_active_tape()
        name = self.__get_name()
        item = QListWidgetItem(name)
        # item.doubleClicked.connect(self.__choose_tape) TODO: не работает, уже погуглил - нужны сигналы
        self.__list.addItem(item)
        self.__tape.reset()
        self.__tapes[name] = dict()
        self.__tapes[name]['widget'] = item
        self.__tapes[name]['state'] = self.__tape.get_data()
        self.__set_active(name)

    def __remove_item(self, name: str) -> None:
        # удаление ленты из списка и из собственного словаря
        self.__list.takeItem(self.__list.row(self.__tapes[name]['widget']))
        self.__tapes.pop(name)

    def __set_inactive(self, name: str) -> None:
        self.__tapes[name]['widget'].setFont(QFont('', italic=False))  # херовый фонт

    def __set_active(self, name: str) -> None:
        # TODO: лучше, чтоб айтем подсвечивался
        self.__active_tape = name
        self.__tapes[name]['widget'].setFont(QFont('', italic=True))  # херовый фонт
        self.__tape.set_from_file(self.__tapes[name]['state'])

    def __set_list(self) -> None:
        self.__list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.__add_item()

    def __set_main_layout(self) -> None:
        self.__main_layout.addWidget(self.__buttons)
        self.__main_layout.addWidget(self.__list)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

    def __draw(self) -> None:
        self.__set_add()
        self.__set_remove()
        self.__set_clear()
        self.__set_buttons_layout()
        self.__set_buttons()
        self.__set_list()
        self.__set_main_layout()
        self.setLayout(self.__main_layout)

    def __on_add_click(self) -> None:
        self.__set_inactive(self.__active_tape)
        self.__add_item()
        self.__tape.reset()

    def __on_remove_click(self) -> None:
        # просто получаем список выделенных и удоляем
        items = self.__list.selectedItems()
        for item in items:
            self.__remove_item(item.text())
        # делаем активной последюю ленту, если она есть
        if (count := self.__list.count()) > 0:
            self.__set_active(self.__list.item(count - 1).text())
        # всегда должна быть хотя бы одна лента, даже если все ленты были удалены
        else:
            self.__add_item()

    def save_active_tape(self) -> None:
        if self.__active_tape in self.__tapes:
            self.__tapes[self.__active_tape]['state'] = self.__tape.get_data()

    def __choose_tape(self) -> None:
        pass
        # if (name := self.__list.selectedItem().text()) != self.__active_tape:
        #     self.__set_active(name)

    def get_data(self) -> dict:
        self.save_active_tape()
        return self.__tapes
