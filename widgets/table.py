from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QCheckBox


# TODO: добавить методы disable и able (чтобы отключать возможность редактирования во время выполнения программы)
# TODO: будет отлично, если при выделении ячейки, также показывалось, на какой следующий стейтмент он указывает


class Table(QWidget):

    def __init__(self, parent: any = None) -> None:
        super().__init__(parent=parent)
        self.__parent = parent
        self.__button_width = 50
        self.__button_height = 25

        self.__insert = QPushButton()
        self.__remove = QPushButton()
        self.__clear = QPushButton()
        self.__shift_mode = QCheckBox()
        self.__buttons = QWidget()
        self.__table = QTableWidget()

        self.__buttons_layout = QHBoxLayout()
        self.__main_layout = QVBoxLayout()

        self.draw()

    def __set_insert(self) -> None:
        self.__insert.setText('Insert')
        self.__insert.setToolTip('')  # TODO: добавить
        self.__insert.setFixedWidth(self.__button_width)
        # TODO: привязять к функции

    def __set_remove(self) -> None:
        self.__remove.setText('Remove')
        self.__remove.setToolTip('')  # TODO: добавить
        self.__remove.setFixedWidth(self.__button_width)
        # TODO: привязять к функции

    def __set_clear(self) -> None:
        self.__clear.setText('Clear')
        self.__clear.setToolTip('')  # TODO: добавить
        self.__clear.setFixedWidth(self.__button_width)
        # TODO: привязять к функции

    def __set_shift_mode(self) -> None:
        self.__shift_mode.setText('Shift')
        self.__shift_mode.setToolTip('Shifts values after <b>insertion</b> or <b>removal</b>')
        # TODO: привязять к функции

    def __set_buttons_layout(self) -> None:
        self.__buttons_layout.addWidget(self.__insert)
        self.__buttons_layout.addWidget(self.__remove)
        self.__buttons_layout.addWidget(self.__clear)
        # просто спейсер, чтобы поставить чекбокс справа
        # spacer = QWidget()
        # spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.__buttons_layout.addWidget(spacer)
        self.__buttons_layout.addWidget(self.__shift_mode)
        self.__buttons_layout.setContentsMargins(0, 0, 0, 0)

    def __set_buttons(self) -> None:
        self.__buttons.setLayout(self.__buttons_layout)
        self.__buttons.setFixedHeight(self.__button_height)

    def __set_table(self) -> None:
        self.__table.setRowCount(4)
        self.__table.setColumnCount(3)
        self.__table.setHorizontalHeaderLabels(["Command", "Jump to state", "Comment"])
        self.__table.cellClicked.connect(self.row_column_clicked)

    def __set_main_layout(self) -> None:
        self.__main_layout.addWidget(self.__buttons)
        self.__main_layout.addWidget(self.__table)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

    def draw(self):
        self.__set_insert()
        self.__set_remove()
        self.__set_clear()
        self.__set_shift_mode()
        self.__set_buttons_layout()
        self.__set_buttons()
        self.__set_table()
        self.__set_main_layout()
        self.setLayout(self.__main_layout)

    def row_column_clicked(self):
        if self.__table.currentRow() + 1 == self.__table.rowCount():
            self.__table.setRowCount(self.__table.rowCount() + 1)

    def add_row(self, i, j, value):
        if self.__table.rowCount() - 1 == i:
            self.__table.setRowCount(i + 1)
        self.__table.setItem(i, j, QTableWidgetItem(value))

    def reset(self):
        self.__table.setRowCount(1)

    def get_data(self) -> dict:
        table_data = dict()
        count_rows = self.__table.rowCount()
        for i in range(count_rows):
            command, comment, jump_state = '', '', ''
            try:
                command = self.__table.item(i, 0).text()
                jump_state = self.__table.item(i, 1).text()
                comment = self.__table.item(i, 2).text()
            except AttributeError:
                pass
            table_data[i] = [command, jump_state, comment]
        return table_data

    def set_from_file(self, file: dict):
        indexes = list(file)
        indexes.sort()
        indexes = list(map(int, indexes))
        for index in indexes:
            if index >= self.__table.rowCount():
                self.__table.setRowCount(index + 1)
            for i in range(3):
                try:
                    self.add_row(index, i, file[str(index)][i])
                except:  # TODO: сделать по канонам ексепшенов
                    self.add_row(index, i, file[index][i])
