from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QCheckBox


# TODO: добавить методы disable и able (чтобы отключать возможность редактирования во время выполнения программы)
# TODO: будет отлично, если при выделении ячейки, также показывалось, на какой следующий стейтмент он указывает


class TableProgram(QWidget):

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.__parent = parent
        self.__buttons_layout = QHBoxLayout()
        self.__buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.__buttons = QWidget()
        self.__buttons.setLayout(self.__buttons_layout)
        self.__buttons.setFixedHeight(25)
        self.table = QTableWidget()

        # TODO: привязять кнопки к функциям
        self.__insert = QPushButton('Insert')
        self.__remove = QPushButton('Remove')
        self.__clear = QPushButton('Clear')
        self.__del_mode = QCheckBox('Shift')
        self.__del_mode.setToolTip('Shifts values after <b>insertion</b> or <b>removal</b>')

        self.__main_layout = QVBoxLayout(self)
        self.__main_layout.addWidget(self.__buttons)
        self.__main_layout.addWidget(self.table)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.__main_layout)

    def draw(self):
        self.__insert.setFixedWidth(50)
        self.__remove.setFixedWidth(50)
        self.__clear.setFixedWidth(50)

        self.__buttons_layout.addWidget(self.__insert)
        self.__buttons_layout.addWidget(self.__remove)
        self.__buttons_layout.addWidget(self.__clear)
        # просто спейсер, чтобы поставить чекбокс справа
        # spacer = QWidget()
        # spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.__buttons_layout.addWidget(spacer)
        self.__buttons_layout.addWidget(self.__del_mode)

        self.table.setRowCount(4)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Command", "Jump to state", "Comment"])
        self.table.cellClicked.connect(self.row_column_clicked)

    def row_column_clicked(self):
        if self.table.currentRow() + 1 == self.table.rowCount():
            self.table.setRowCount(self.table.rowCount() + 1)

    def add_row(self, i, j, value):
        if self.table.rowCount() - 1 == i:
            self.table.setRowCount(i + 1)
        self.table.setItem(i, j, QTableWidgetItem(value))

    def reset(self):
        self.table.setRowCount(1)

    def set_from_file(self, file: dict):
        indexes = list(file)
        indexes.sort()
        indexes = list(map(int, indexes))
        for index in indexes:
            if index >= self.table.rowCount():
                self.table.setRowCount(index + 1)
            for i in range(3):
                try:
                    self.table.add_row(index, i, file[str(index)][i])
                except:
                    self.table.add_row(index, i, file[index][i])
