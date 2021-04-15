import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QDoubleSpinBox, QMainWindow, QAction,
                             QToolBar, QGridLayout, QSizePolicy, QSplitter, QLabel)

from post_machine_logic import Runner
from table_program import TableProgram
from tape_list import TapeList
from tape import Tape
from utils import Loader
from utils import Saver


# TODO: во время (не) выполнения программы некоторые элементы должны быть не активными


class App(QMainWindow):
    signal_mark_carriage = QtCore.pyqtSignal()
    signal_unmark_carriage = QtCore.pyqtSignal()
    signal_go_right = QtCore.pyqtSignal()
    signal_go_left = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.__main_widget = QWidget()
        self.__main_layout = QGridLayout(self.__main_widget)

        self.__run_action:   QAction
        self.__stop_action:  QAction
        self.__debug_action: QAction
        self.__save_action:  QAction
        self.__load_action:  QAction
        self.__reset_action: QAction
        self.__exit_action:  QAction
        self.__timer: QDoubleSpinBox

        self.__menu_bar = self.menuBar()
        self.__file_menu = self.__menu_bar.addMenu('&File')
        # TODO: добавить ещё нужные меню

        self.__upper_toolbar = QToolBar()
        self.__lower_toolbar = QToolBar()

        # основные экраны приложения
        # TODO: исправить баг со сплиттером - при чрезмерном сдвиге в сторону, виджет в той же стороне исчезает
        # ^ хотя его можно вернуть - может быть это просто фича такая?
        self.__upper_level = QSplitter(QtCore.Qt.Horizontal)
        self.__table_program = TableProgram(self)
        self.__tape_list = TapeList(self)
        self.__tape = Tape(self)
        self.__last_state = QLabel(self)

        self.signal_mark_carriage.connect(self.__tape.mark_carriage)
        self.signal_unmark_carriage.connect(self.__tape.unmark_carriage)
        self.signal_go_right.connect(self.__tape.go_right)
        self.signal_go_left.connect(self.__tape.go_left)
        # TODO: пипец там инкапсуляции ноль, поэтому всё ломается мгновенно при создании раннера
        # self.runner = Runner(self)

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

    def __set_toolbars(self) -> None:
        # TODO: понять почему левый и верхний ContentMargin не работают (нижний и правый работают)
        # ^ на всякий случай можно поставить спейсер, наверно
        # установка тулбаров
        self.addToolBar(Qt.TopToolBarArea, self.__upper_toolbar)
        self.addToolBar(Qt.BottomToolBarArea, self.__lower_toolbar)
        self.__lower_toolbar.setMovable(False)

        # настройка верхнего тулбара
        self.__upper_toolbar.setMovable(False)
        self.__upper_toolbar.addAction(self.__run_action)
        self.__upper_toolbar.addAction(self.__stop_action)
        # TODO: добавить остальные кнопки
        self.__upper_toolbar.addSeparator()

        self.__timer = QDoubleSpinBox(self)
        self.__timer.setRange(0.05, 1)
        self.__timer.setDecimals(2)
        self.__timer.setSingleStep(0.05)
        self.__timer.setSuffix(' sec')
        self.__timer.setFixedSize(80, 20)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.__upper_toolbar.addWidget(spacer)
        self.__upper_toolbar.addWidget(QLabel('Speed: '))
        self.__upper_toolbar.addWidget(self.__timer)
        self.__upper_toolbar.setContentsMargins(0, 0, 5, 0)  # TODO: нормально подравнять нужно

        # настройка нижнего тулбара
        self.__lower_toolbar.setMovable(False)
        self.__lower_toolbar.addWidget(self.__last_state)

        # TODO: наверно стоит увеличить размер шрифта
        self.__last_state.setText('  Application loaded')  # TODO: убрать хардкод
        self.__last_state.setFixedHeight(15)

    def __set_upper_level(self) -> None:
        self.__upper_level.addWidget(self.__table_program)
        self.__upper_level.addWidget(self.__tape_list)
        self.__upper_level.setStretchFactor(1, 0)
        self.__upper_level.setSizes([750, 150])
        # TODO: надо сделать так, чтоб при расширении окна, приоритет расширения всегда был только на таблицу

    def __set_interface(self) -> None:
        self.__table_program.draw()
        self.__tape.draw(self.size().width())

        self.__set_upper_level()

        self.__main_layout.addWidget(self.__upper_level)
        self.__main_layout.addWidget(self.__tape)
        self.__tape.setFixedHeight(140)  # TODO: когда починится лента, то значение нужно уменьшить до 80

        self.__main_layout.addWidget(self.__main_widget, 0, 0)

    # def set_buttons(self, name: str, hint: str, x: int, y: int):
    #     self.buttons[f'{name}'] = QPushButton(name, self)
    #     self.buttons[f'{name}'].setToolTip(hint)
    #     self.buttons[f'{name}'].resize(80, 25)
    #     self.buttons[f'{name}'].move(x, y)

    # def set_actions_buttons(self):
    #     self.buttons['Save'].clicked.connect(lambda: Saver.save_program(self))
    #     self.buttons['Load'].clicked.connect(lambda: Loader.load_program(self))
    #     self.buttons['Start'].clicked.connect(self.run_program)
    #     self.buttons['Stop'].clicked.connect(self.stop_program)
    #     self.buttons['Reset tape'].clicked.connect(lambda: self.__tape.reset())

    def run_program(self):
        self.runner.start()

    def stop_program(self):
        program = self.runner.program
        self.runner.stop_program = True
        self.runner.quit()
        self.runner.wait()
        Loader.load_program_from_dict(program, self)

    def initUI(self):
        self.setGeometry(200, 200, 900, 500)
        self.setWindowTitle('Post Machine')

        self.__set_actions()
        self.__set_menu_bar()
        self.__set_toolbars()
        self.__set_interface()

        self.setCentralWidget(self.__main_widget)
        self.show()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Resize:
            self.__tape.resize(self.size().width())
        return super().eventFilter(obj, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    App = App()
    sys.exit(app.exec_())
