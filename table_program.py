from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem

# TODO засунуть в LAYOUT


class TableProgram:

    def __init__(self, app: QWidget, x: int, y: int) -> None:
        self.__app = app
        self.__x = x
        self.__y = y
        self.table = QTableWidget(self.__app)

    def create_table(self):
        self.table.setRowCount(4)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Command", "Jump to state", "Comment"])
        self.table.cellClicked.connect(self.row_column_clicked)
        self.table.resize(800, 600)
        self.table.move(self.__x, self.__y)

    def row_column_clicked(self):
        if self.table.currentRow() + 1 == self.table.rowCount():
            self.table.setRowCount(self.table.rowCount() + 1)

    def add_row(self, i, j, value):
        if self.table.rowCount() - 1 == i:
            self.table.setRowCount(i + 1)
        self.table.setItem(i, j, QTableWidgetItem(value))

    def set_from_file(self, file: dict):
        indexes = list(file)
        indexes.sort()
        indexes = list(map(int, indexes))
        for index in indexes:
            if index >= self.table.rowCount():
                self.table.setRowCount(index + 1)
            for i in range(3):
                try:
                    self.add_row(index, i, file[str(index)][i])
                except:
                    self.add_row(index, i, file[index][i])
