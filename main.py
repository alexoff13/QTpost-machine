import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QApplication, QPushButton, QDoubleSpinBox)

from post_machine_logic import Runner
from table_program import TableProgram
from tape import Tape
from utils import Loader
from utils import Saver


class App(QWidget):
    signal_mark_carriage = QtCore.pyqtSignal()
    signal_unmark_carriage = QtCore.pyqtSignal()
    signal_go_right = QtCore.pyqtSignal()
    signal_go_left = QtCore.pyqtSignal()

    def __init__(self):

        super().__init__()
        self.tape = Tape(self)
        self.table_program = TableProgram(self, 10, 80)
        self.buttons = dict()

        self.signal_mark_carriage.connect(self.tape.mark_carriage)
        self.signal_unmark_carriage.connect(self.tape.unmark_carriage)
        self.signal_go_right.connect(self.tape.go_right)
        self.signal_go_left.connect(self.tape.go_left)
        self.runner = Runner(self)
        self.installEventFilter(self)
        self.initUI()

    def set_buttons(self, name: str, hint: str, x: int, y: int):
        self.buttons[f'{name}'] = QPushButton(name, self)
        self.buttons[f'{name}'].setToolTip(hint)
        self.buttons[f'{name}'].resize(80, 25)
        self.buttons[f'{name}'].move(x, y)

    def set_actions_buttons(self):
        self.buttons['Save'].clicked.connect(lambda: Saver.save_program(self))
        self.buttons['Load'].clicked.connect(lambda: Loader.load_program(self))
        self.buttons['Start'].clicked.connect(self.run_program)
        self.buttons['Stop'].clicked.connect(self.stop_program)

    def run_program(self):
        self.runner.start()

    def stop_program(self):
        program = self.runner.program
        self.runner.terminate()
        Loader.load_program_from_dict(program, self)

    def initUI(self):
        # установка параметров окна
        self.setGeometry(200, 200, 900, 500)
        self.setWindowTitle('Post Machine')

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
        self.buttons['timer'] = QDoubleSpinBox(self)
        self.buttons['timer'].setRange(0.1, 1)
        self.buttons['timer'].setDecimals(1)
        self.buttons['timer'].setSingleStep(0.1)
        self.buttons['timer'].resize(80, 20)
        self.buttons['timer'].move(x, y)

        # установка ленты
        self.tape.draw(self.size().width())

        # установка таблицы с программой
        self.table_program.create_table()

        self.show()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Resize:
            self.tape.resize(self.size().width())
        return super().eventFilter(obj, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    App = App()
    sys.exit(app.exec_())
