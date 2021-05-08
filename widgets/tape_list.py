from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QListWidgetItem

from widgets.tests_list import TestsList
from widgets.main_list import MainList
from widgets.tape import Tape


class TapeList(QWidget):
    def __init__(self, tape: Tape, parent: any = None):
        super().__init__(parent=parent)
        self.__tape = tape
        self.__parent = parent
        self.__button_width = 60
        self.__button_height = 25
        self.__active_tape = None
        
        self.__add = QPushButton()
        self.__remove = QPushButton()
        self.__buttons = QWidget()
        self.__tests_list = TestsList(self.__tape)
        self.__main_list = MainList(self.__tape)

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
        self.__add.setFixedWidth(self.__button_width)
        self.__add.clicked.connect(self.__on_add_click)

    def __set_remove(self) -> None:
        self.__remove.setText('Remove')
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

    def __set_tests(self) -> None:
        self.__tests_list.itemClicked.connect(self.__choose_tape)
        self.__tests_list.itemChanged.connect(self.__check_item)

    def __set_main(self) -> None:
        self.__main_list.itemClicked.connect(self.__choose_tape)
        self.__set_active(self.__main_list.main, False)

    def __set_main_layout(self) -> None:
        self.__main_layout.addWidget(self.__buttons)
        self.__main_layout.addWidget(self.__tests_list)
        self.__main_layout.addWidget(self.__main_list)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

    def __draw(self) -> None:
        self.__set_buttons_layout()
        self.__set_buttons()
        self.__set_tests()
        self.__set_main()
        self.__set_main_layout()
        self.setLayout(self.__main_layout)

    def __set_inactive(self, item: QListWidgetItem) -> None:
        self.save_active_tape()
        item.setFont(self.__inactive_font)

    def __set_active(self, item: QListWidgetItem, set_tape: bool = True) -> None:
        self.__active_tape = item
        item.setFont(self.__active_font)
        if set_tape:
            if item == self.__main_list.main:
                self.__tape.set_from_file(self.__main_list.state)
            else:
                self.__tape.set_from_file(self.__tests_list.get_state(item))

    def __remove_item(self, item: QListWidgetItem) -> None:
        self.__tests_list.remove_test(item)

    def __on_add_click(self) -> None:
        self.__set_inactive(self.__active_tape)
        self.__set_active(self.__tests_list.add_test())
        self.__tape.reset()

    def __on_remove_click(self) -> None:
        # просто получаем список выделенных и удаляем
        tests = self.__tests_list.selectedItems()
        if len(tests) > 0:
            for test in tests:
                self.__remove_item(test)
            # делаем активной последюю ленту, если она есть
            if self.__main_list.main != self.__active_tape and self.__tests_list.get_last() is not None:
                self.__set_active(self.__tests_list.get_last())
            else:
                self.__set_active(self.__main_list.main)

    def __choose_tape(self, item: QListWidgetItem) -> None:
        if item != self.__active_tape:
            self.__set_inactive(self.__active_tape)
            self.__set_active(item)

    def __check_item(self, item: QListWidgetItem) -> None:
        try:
            item.last_name
        except AttributeError:
            if self.__main_list.last_time_dragged > self.__tests_list.last_time_dragged:
                test_name = self.__tests_list.get_test_name(item.text())
                # TODO: но таким образом он добавляет всегда в конец
                test = self.__tests_list.add_test(test_name, state=self.get_main_data(), reset=False)
                self.__set_inactive(test)
            self.__tests_list.remove_test(item, False)
        else:
            test_name = item.text()
            if item.last_name != test_name:
                correct_name = self.__tests_list.get_test_name(test_name, item.last_name)
                if test_name != correct_name:
                    item.setText(correct_name)
                self.__tests_list.rename(item.last_name, correct_name)

    def save_active_tape(self) -> None:
        if self.__active_tape == self.__main_list.main:
            self.__main_list.save_state()
        else:
            self.__tests_list.save_state(self.__active_tape)

    def get_main_data(self) -> dict:
        self.save_active_tape()
        return self.__main_list.state

    def get_tests_data(self) -> dict:
        self.save_active_tape()
        return self.__tests_list.get_data()

    def set_main_from_file(self, file: dict) -> None:
        if self.__active_tape == self.__main_list.main:
            self.__tape.set_from_file(file)
        else:
            self.__main_list.state = file

    def set_tests_from_file(self, file: dict) -> None:
        self.__tests_list.set_from_file(file)

    def has_main_unsaved_data(self) -> bool:
        self.save_active_tape()
        return self.__main_list.has_unsaved_data()

    def has_tests_unsaved_data(self) -> bool:
        self.save_active_tape()
        return self.__tests_list.has_unsaved_data()
