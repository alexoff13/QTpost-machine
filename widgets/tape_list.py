from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QListWidget, QListWidgetItem, \
    QAbstractItemView

from widgets.tape import Tape


class TapeList(QWidget):
    DEFAULT_NAME = 'tape'

    def __init__(self, tape: Tape, parent: any = None):
        super().__init__(parent=parent)
        self.__tape = tape
        self.__parent = parent
        self.__button_width = 50
        self.__button_height = 25
        self.__tapes = dict()
        self.__active_tape = self.DEFAULT_NAME
        
        self.__add = QPushButton()
        self.__remove = QPushButton()
        self.__buttons = QWidget()
        self.__list = QListWidget()

        self.__buttons_layout = QHBoxLayout()
        self.__main_layout = QVBoxLayout()

        self.__active_font = QFont()
        self.__inactive_font = QFont()
        self.__set_fonts()

        self.__draw()

    def __set_fonts(self) -> None:
        self.__active_font.setBold(True)

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

    def __set_buttons_layout(self) -> None:
        self.__buttons_layout.addWidget(self.__add)
        self.__buttons_layout.addWidget(self.__remove)
        self.__buttons_layout.setAlignment(Qt.AlignLeft)
        self.__buttons_layout.setContentsMargins(0, 0, 0, 0)

    def __set_buttons(self) -> None:
        self.__set_add()
        self.__set_remove()
        self.__buttons.setLayout(self.__buttons_layout)
        self.__buttons.setFixedHeight(self.__button_height)

    def __set_list(self) -> None:
        # устанавливает возможность сразу нескольких элементов
        self.__list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # устанавливает возможность двойного клика на элемент
        self.__list.itemClicked.connect(self.__choose_tape)
        # устанавливает возможность Drag'n'Drop элементов
        self.__list.setDragDropMode(QAbstractItemView.InternalMove)
        self.__list.setDropIndicatorShown(True)
        # устанавливает нужные триггеры для изменения имени элемента
        self.__list.itemChanged.connect(self.__check_item)

        self.__add_item()

    def __set_main_layout(self) -> None:
        self.__main_layout.addWidget(self.__buttons)
        self.__main_layout.addWidget(self.__list)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

    def __draw(self) -> None:
        self.__set_buttons_layout()
        self.__set_buttons()
        self.__set_list()
        self.__set_main_layout()
        self.setLayout(self.__main_layout)

    def __get_tape_name(self, name: str = DEFAULT_NAME, ignore_name: str = None) -> str:
        if not name:
            name = self.DEFAULT_NAME
        k = 1
        new_name = name
        while new_name in self.__tapes and new_name != ignore_name:
            new_name = f'{name}-{k}'
            k += 1
        return new_name

    def __set_inactive(self, name: str) -> None:
        self.save_active_tape()
        self.__tapes[name]['widget'].setFont(self.__inactive_font)

    def __set_active(self, name: str, set_tape: bool = True) -> None:
        self.__active_tape = name
        self.__tapes[name]['widget'].setFont(self.__active_font)
        if set_tape:
            self.__tape.set_from_file(self.__tapes[name]['state'])

    def __add_item(self, name: str = None, state: dict = None, set_active: bool = True) -> None:
        if name is None:
            name = self.__get_tape_name()
        item = QListWidgetItem(name)
        item.last_name = name
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.save_active_tape()
        self.__list.addItem(item)
        self.__tape.reset()
        self.__tapes[name] = dict()
        self.__tapes[name]['widget'] = item
        self.__tapes[name]['state'] = state
        if set_active:
            self.__set_active(name, False)

    def __remove_item(self, name: str) -> None:
        # удаление ленты из списка и из собственного словаря
        self.__list.takeItem(self.__list.row(self.__tapes[name]['widget']))
        self.__tapes.pop(name)

    def __on_add_click(self) -> None:
        self.__set_inactive(self.__active_tape)
        self.__add_item()
        self.__tape.reset()

    def __on_remove_click(self) -> None:
        # просто получаем список выделенных и удаляем
        items = self.__list.selectedItems()
        if len(items) > 0:
            for item in items:
                self.__remove_item(item.text())
            # делаем активной последюю ленту, если она есть
            if (count := self.__list.count()) > 0:
                self.__set_active(self.__list.item(count - 1).text())
            # всегда должна быть хотя бы одна лента, даже если все ленты были удалены
            else:
                self.__add_item()

    def __choose_tape(self, item: QListWidgetItem) -> None:
        name = item.text()
        self.__last_selected_item = name
        if name != self.__active_tape:
            self.__set_inactive(self.__active_tape)
            self.__set_active(name)

    def __check_item(self, item: QListWidgetItem) -> None:
        # ============================================== костыль ==============================================
        # не знаю почему, но иногда в событие передается какой-то item (элемент списка), который я НЕ создавал,
        # поэтому приходится его добавлять в свой список и ставить нужные настройки
        try:
            item.last_name
        except AttributeError:
            item.last_name = item.text()
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            item.setFont(self.__active_font if item.last_name == self.__active_tape else self.__inactive_font)
            self.__tapes[item.last_name]['widget'] = item
        # =====================================================================================================
        # проверка, изменил ли элемент свое имя
        if item.last_name != item.text():
            correct_name = self.__get_tape_name(item.text(), item.last_name)
            if item.text() != correct_name:
                item.setText(correct_name)
            if item.last_name == self.__active_tape:
                self.__active_tape = correct_name
            self.__tapes[correct_name] = self.__tapes.pop(item.last_name)
            item.last_name = correct_name

    def save_active_tape(self) -> None:
        if self.__active_tape in self.__tapes:
            self.__tapes[self.__active_tape]['state'] = self.__tape.get_data()

    def get_data(self) -> dict:
        self.save_active_tape()
        data = dict()
        # TODO: иногда данные могут сохраняться не так, как находятся в списке -> неверное отображение при загрузке
        for name in self.__tapes:
            data[name] = self.__tapes[name]['state']
        return data

    # TODO: возможно лучше предложить выбор: загрузка с заменой или с добавлением в конец
    def set_from_file(self, file: dict) -> None:
        for name in list(self.__tapes.keys()):
            self.__remove_item(name)
        for name in file:
            self.__add_item(name, file[name], False)
        # вдруг кто-то зайдет в .pmt и удалит все ленты
        if (count := self.__list.count()) == 0:
            self.__add_item()
        else:
            self.__set_active(self.__list.item(count - 1).text())

    def has_unsaved_data(self) -> bool:
        return len(self.__tapes) > 1 or self.DEFAULT_NAME not in self.__tapes or \
               self.__tapes[self.DEFAULT_NAME]['state'] is not None and self.__tape.has_unsaved_data()
