import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QApplication, QPushButton, QDoubleSpinBox, QMainWindow, QAction, QHBoxLayout, QVBoxLayout,
                             QMenu, QToolBar, QGridLayout, QLayout, QTabWidget)

from post_machine_logic import Runner
from table_program import TableProgram
from tape import Tape
from utils import Loader
from utils import Saver


class App(QMainWindow):
    signal_mark_carriage = QtCore.pyqtSignal()
    signal_unmark_carriage = QtCore.pyqtSignal()
    signal_go_right = QtCore.pyqtSignal()
    signal_go_left = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.__main_widget = QWidget(self)
        self.__main_layout = QGridLayout(self.__main_widget)
        self.__interface = QVBoxLayout()

        self.__run_action:   QAction
        self.__stop_action:  QAction
        self.__debug_action: QAction
        self.__save_action:  QAction
        self.__load_action:  QAction
        self.__reset_action: QAction
        self.__exit_action:  QAction

        self.__menu_bar = self.menuBar()
        self.__file_menu = self.__menu_bar.addMenu('&File')
        # TODO: добавить ещё нужные меню

        self.__toolbar = QToolBar()
        # TODO: добавить ещё нужные действия

        self.__table_program = TableProgram(self)
        self.__tape = Tape(self)
        self.__terminal = QWidget(self)  # TODO: создать нормальный класс для терминала (наследник QWidget)

        self.__tape_terminal_tab = QTabWidget()
        # self.table_program = TableProgram(self)
        # self.buttons = dict()

        self.signal_mark_carriage.connect(self.__tape.mark_carriage)
        self.signal_unmark_carriage.connect(self.__tape.unmark_carriage)
        self.signal_go_right.connect(self.__tape.go_right)
        self.signal_go_left.connect(self.__tape.go_left)
        #self.runner = Runner(self)

        self.installEventFilter(self)
        self.initUI()

    def __set_actions(self) -> None:
        self.__run_action = QAction(QIcon('icons/run-button.png'), 'Run', self)
        self.__run_action.setShortcut('Ctrl+R')
        self.__run_action.setStatusTip('Start program')
        self.__run_action.triggered.connect(self.run_program)

        self.__stop_action = QAction(QIcon('icons/stop-button.png'), 'Stop', self)
        self.__stop_action.setShortcut('Ctrl+S')
        self.__stop_action.setStatusTip('Stop program')
        self.__stop_action.triggered.connect(self.stop_program)

        # TODO: добавить остальные действия

        self.__exit_action = QAction(QIcon(''), 'Exit', self)
        self.__exit_action.setShortcut('Ctrl+Q')
        self.__exit_action.setStatusTip('Exit application')
        self.__exit_action.triggered.connect(self.close)

    def __set_menu_bar(self) -> None:
        self.statusBar()

        self.__file_menu.addAction(self.__run_action)
        self.__file_menu.addAction(self.__stop_action)
        self.__file_menu.addSeparator()
        self.__file_menu.addAction(self.__exit_action)
        # TODO: добавить остальные вкладки

    def __set_tool_bar(self) -> None:
        self.__toolbar = self.addToolBar('')
        self.__toolbar.setMovable(False)

        self.__toolbar.addAction(self.__run_action)
        self.__toolbar.addAction(self.__stop_action)
        # TODO: добавить остальные кнопки

    def __set_interface(self) -> None:
        self.__table_program.create_table()
        self.__tape.draw(self.size().width())

        self.__tape_terminal_tab.addTab(QWidget(self), 'Tape')  # TODO: вставить нормальный класс Tape
        self.__tape_terminal_tab.addTab(self.__terminal, 'Terminal')

        self.__main_layout.addWidget(self.__table_program, 0, 0)
        self.__main_layout.addWidget(self.__tape_terminal_tab, 1, 0)

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
        self.buttons['Reset tape'].clicked.connect(lambda: self.__tape.reset())

    def run_program(self):
        self.runner.start()

    def stop_program(self):
        program = self.runner.program
        self.runner.stop_program = True
        self.runner.quit()
        self.runner.wait()
        Loader.load_program_from_dict(program, self)

    def initUI(self):
        self.__set_actions()
        self.__set_menu_bar()
        self.__set_tool_bar()
        self.__set_interface()

        self.__main_layout.sizeConstraint = QLayout.SetDefaultConstraint
        self.setCentralWidget(self.__main_widget)


        # установка параметров окна
        self.setGeometry(200, 200, 900, 500)
        self.setWindowTitle('Post Machine')

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        # установка ленты
        # self.tape.draw(self.size().width())

        # установка таблицы с программой
        # self.table_program.create_table()

        # установка верхних главных кнопок
        # x, y = 10, 10
        # for name in ('Start', 'Debug', 'Stop', 'Save', 'Load', 'Reset tape'):
        #     self.set_buttons(name, name, x, y)
        #     x += 80
        # # установка действий главных кнопок
        # self.set_actions_buttons()

        # установка таймера
        # self.buttons['timer'] = QDoubleSpinBox(self)
        # self.buttons['timer'].setRange(0.1, 1)
        # self.buttons['timer'].setDecimals(1)
        # self.buttons['timer'].setSingleStep(0.1)
        # self.buttons['timer'].resize(80, 20)
        # self.buttons['timer'].move(x, y)

        self.show()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Resize:
            self.__tape.resize(self.size().width())
        return super().eventFilter(obj, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    App = App()
    sys.exit(app.exec_())
