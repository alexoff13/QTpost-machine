import sys
import threading

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QApplication, QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, QGridLayout, QLabel,
                             QDoubleSpinBox, QMainWindow)
from PyQt5 import QtGui
from commands import Runner
from table_program import TableProgram
from tape import Tape
from utils.loader import Loader
from utils.saver import Saver


class App(QWidget):

    Signal_inverse_carriage = QtCore.pyqtSignal()
    Signal_inverse_carriage_false = QtCore.pyqtSignal()
    Signal_go_right = QtCore.pyqtSignal()
    Signal_go_left = QtCore.pyqtSignal()

    def __init__(self):

        super().__init__()
        self.tape = Tape(self)
        self.table_program = TableProgram(self, 10, 80)
        self.buttons = dict()

        self.Signal_inverse_carriage.connect(lambda: self.tape.inverse_carriage())
        self.Signal_inverse_carriage_false.connect(lambda: self.tape.inverse_carriage(False))
        self.Signal_go_right.connect(lambda: self.tape.go_right())
        self.Signal_go_left.connect(lambda: self.tape.go_left())
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
        self.buttons['Start'].clicked.connect(lambda: self.run_program())
        self.buttons['Stop'].clicked.connect(lambda : self.stop_program())

    def run_program(self):
        self.runner = Runner(self)
        self.runner.start()

    def stop_program(self):
        program = self.runner.program
        self.runner.terminate()
        Loader.load_program_from_dict(program, self)
        # self.runner.wait()

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
