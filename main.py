import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QApplication, QPushButton, QTableWidget, QTableWidgetItem, QSpinBox)

from table_program import TableProgram
from tape import Tape
from utils.loader import Loader
from utils.saver import Saver


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.buttons = dict()
        self.initUI()

    def set_buttons(self, name: str, hint: str, x: int, y: int):
        self.buttons[f'{name}'] = QPushButton(name, self)
        self.buttons[f'{name}'].setToolTip(hint)
        self.buttons[f'{name}'].resize(self.buttons[f'{name}'].sizeHint())
        self.buttons[f'{name}'].move(x, y)

    def set_actions_buttons(self):
        self.buttons['Save'].clicked.connect(lambda: Saver.save_program(self))
        self.buttons['Load'].clicked.connect(lambda: Loader.load_program(self))

    def initUI(self):
        # установка верхних главных кнопок
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')
        x, y = 10, 10
        for name in ('Start', 'Debug', 'Stop', 'Save', 'Load'):
            self.set_buttons(name, name, x, y)
            x += 80
        # установка действий главных кнопок
        self.set_actions_buttons()
        # установка таймера
        self.buttons['timer'] = QSpinBox(self)
        self.buttons['timer'].resize(80, 20)
        self.buttons['timer'].move(x, y)

        # установка ленты
        self.tape = Tape(self, 10, 50)
        self.tape.show()

        # установка таблицы с программой
        self.table_program = TableProgram(self, 10, 80)
        self.table_program.create_table()

        # установка параметров окна
        self.setGeometry(200, 200, 900, 500)
        self.setWindowTitle('Post Machine')

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    App = App()
    sys.exit(app.exec_())
