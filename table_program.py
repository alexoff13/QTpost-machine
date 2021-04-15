from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMainWindow


# TODO засунуть в LAYOUT


class TableProgram(QTableWidget):

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.__parent = parent

    def create_table(self):
        self.setRowCount(4)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Command", "Jump to state", "Comment"])
        self.cellClicked.connect(self.row_column_clicked)
        # self.resize(800, 600)

    def row_column_clicked(self):
        if self.currentRow() + 1 == self.rowCount():
            self.setRowCount(self.rowCount() + 1)

    def add_row(self, i, j, value):
        if self.rowCount() - 1 == i:
            self.setRowCount(i + 1)
        self.setItem(i, j, QTableWidgetItem(value))

    def reset(self):
        self.setRowCount(1)

    def set_from_file(self, file: dict):
        indexes = list(file)
        indexes.sort()
        indexes = list(map(int, indexes))
        for index in indexes:
            if index >= self.rowCount():
                self.setRowCount(index + 1)
            for i in range(3):
                try:
                    self.add_row(index, i, file[str(index)][i])
                except:
                    self.add_row(index, i, file[index][i])
