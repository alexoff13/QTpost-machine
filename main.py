import sys

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon, QImage, QPixmap, QCloseEvent
from PyQt5.QtWidgets import (QWidget, QApplication, QDoubleSpinBox, QMainWindow, QAction,
                             QToolBar, QGridLayout, QSizePolicy, QSplitter, QLabel, QLineEdit, QFrame, QMessageBox,
                             QDialog)

from post_machine_logic import Program
from utils import Saver, Loader
from utils.signals import ProgramSignals
from widgets.comment import Comment
from widgets.table import Table
from widgets.tape import Tape
from widgets.tape_list import TapeList


# TODO: во время (не) выполнения программы некоторые элементы должны быть не активными


class App(QMainWindow):
    __signals = ProgramSignals()

    def __init__(self):
        super().__init__()

        # значения окна
        self.__x = 200
        self.__y = 200
        self.__width = 900
        self.__height = 500
        # инициализация главного виджета и слоя для него
        self.__main_widget = QWidget()
        self.__main_layout = QGridLayout(self.__main_widget)
        # инициализация действий и виджетов для тулбаров
        self.__run_action = QAction()
        self.__debug_action = QAction()
        self.__pause_action = QAction()
        self.__stop_action = QAction()
        self.__clear_tape_action = QAction()
        self.__save_program_action = QAction()
        self.__save_tests_action = QAction()
        self.__save_all_action = QAction()
        self.__load_program_action = QAction()
        self.__load_tests_action = QAction()
        self.__reset_action = QAction()
        self.__exit_action = QAction()
        self.__timer = QDoubleSpinBox()
        # инициализация меню
        self.__menu_bar = self.menuBar()
        self.__file_menu = self.__menu_bar.addMenu(str())
        self.__execution_menu = self.__menu_bar.addMenu(str())
        # TODO: добавить ещё нужные меню
        # инициализация тулбара
        self.__toolbar = QToolBar()
        self.__status_bar_label = QLabel()
        self.__status_bar_icon = QLabel()
        # инициализация основых элементов экрана
        # TODO: исправить баг со сплиттером - при чрезмерном сдвиге в сторону, виджет в той же стороне исчезает
        # ^ хотя его можно вернуть - может быть это просто фича такая?
        self.__h_splitter = QSplitter(Qt.Horizontal)  # горизонтальный сплиттер
        self.__v_splitter = QSplitter(Qt.Vertical)  # вертикальный сплиттер
        self.__comment = Comment()
        self.__table = Table()
        self.__tape = Tape(self.__width)
        self.__tape_list = TapeList(self.__tape)
        # инициализация иконок
        self.__OK = QPixmap('icons/ok.png')
        self.__ERROR = QPixmap('icons/error.png')
        self.__RUN = QIcon('icons/run.png')
        self.__PAUSE = QIcon('icons/pause.png')

        # инициализация раннера, сейвера и загрузчика
        self.__saver = Saver(self, self.__comment, self.__table, self.__tape, self.__tape_list)
        self.__loader = Loader(self, self.__comment, self.__table, self.__tape, self.__tape_list, self.__saver)
        self.__program = Program(self.__table, self.__tape, self.__timer, self.__signals.on_stop)

        # установка получения событий
        self.installEventFilter(self)
        # установка пиксельмэпов
        self.__set_pixmaps()
        # инициализация пользовательского интерфейса
        self.init_ui()
        # установка сигналов
        self.__set_signals()

    def __set_pixmaps(self) -> None:
        self.__OK = self.__OK.scaled(20, 20)
        self.__ERROR = self.__ERROR.scaled(20, 20)

    def __set_signals(self) -> None:
        self.__signals.on_stop.connect(self.__enable_interface)

    def __set_run_action(self) -> None:
        self.__run_action.setIcon(QIcon('icons/run.png'))
        self.__run_action.setText('Run')
        self.__run_action.setShortcut('F4')
        self.__run_action.setStatusTip('Run program')
        self.__run_action.triggered.connect(self.run_program)

    def __set_debug_action(self) -> None:
        self.__debug_action.setIcon(QIcon('icons/debug.png'))
        self.__debug_action.setText('Debug')
        self.__debug_action.setShortcut('F8')
        self.__debug_action.setStatusTip('Debug program by step')
        self.__debug_action.triggered.connect(self.debug_program)

    def __set_pause_action(self) -> None:
        self.__pause_action.setIcon(QIcon('icons/pause.png'))
        self.__pause_action.setText('Pause')
        self.__pause_action.setShortcut('F4')  # TODO второй F4
        self.__pause_action.setStatusTip('Pause program')
        self.__pause_action.triggered.connect(self.pause_program)

    def __set_clear_tape_action(self) -> None:
        self.__clear_tape_action.setIcon(QIcon('icons/clear-tape.png'))
        self.__clear_tape_action.setText('Clear')
        self.__clear_tape_action.setShortcut('F9')
        self.__clear_tape_action.setStatusTip('Clear tape')
        self.__clear_tape_action.triggered.connect(self.clear_tape)

    def __set_stop_action(self) -> None:
        self.__stop_action.setIcon(QIcon('icons/stop.png'))
        self.__stop_action.setText('Stop')
        self.__stop_action.setShortcut('F5')
        self.__stop_action.setStatusTip('Stop program')
        self.__stop_action.triggered.connect(self.stop_program)

    def __set_exit_action(self) -> None:
        self.__exit_action.setIcon(QIcon(''))
        self.__exit_action.setText('Exit')
        self.__exit_action.setShortcut('Ctrl+A+D')
        self.__exit_action.setStatusTip('Exit application')
        self.__exit_action.triggered.connect(self.closeEvent)

    def __set_save_program_action(self) -> None:
        self.__save_program_action.setIcon(QIcon('icons/save-program.png'))
        self.__save_program_action.setText('Save Program')
        self.__save_program_action.setShortcut('Ctrl+P')
        self.__save_program_action.setStatusTip('Save Program')
        self.__save_program_action.triggered.connect(self.__saver.save_program)

    def __set_save_tests_action(self) -> None:
        self.__save_tests_action.setIcon(QIcon('icons/save-tests.png'))
        self.__save_tests_action.setText('Save Tests')
        self.__save_tests_action.setShortcut('Ctrl+T')
        self.__save_tests_action.setStatusTip('Save Tests')
        self.__save_tests_action.triggered.connect(self.__saver.save_tests)

    def __set_save_all_action(self) -> None:
        self.__save_all_action.setIcon(QIcon('icons/save-all.png'))
        self.__save_all_action.setText('Save All')
        self.__save_all_action.setShortcut('Ctrl+A')
        self.__save_all_action.setStatusTip('Save All')
        self.__save_all_action.triggered.connect(self.__saver.save_all)

    def __set_load_program_action(self) -> None:
        self.__load_program_action.setIcon(QIcon('icons/open-program.png'))
        self.__load_program_action.setText('Load Program')
        self.__load_program_action.setShortcut('Ctrl+Shift+P')
        self.__load_program_action.setStatusTip('Load Program')
        self.__load_program_action.triggered.connect(self.__loader.load_program)

    def __set_load_tests_action(self) -> None:
        self.__load_tests_action.setIcon(QIcon('icons/open-tests.png'))
        self.__load_tests_action.setText('Load Tests')
        self.__load_tests_action.setShortcut('Ctrl+Shift+T')
        self.__load_tests_action.setStatusTip('Load Tests')
        self.__load_tests_action.triggered.connect(self.__loader.load_tests)

    def __set_actions(self) -> None:
        self.__set_run_action()
        self.__set_debug_action()
        self.__set_pause_action()
        self.__set_stop_action()
        self.__set_save_program_action()
        self.__set_clear_tape_action()
        self.__set_save_tests_action()
        self.__set_save_all_action()
        self.__set_load_program_action()
        self.__set_load_tests_action()
        self.__set_exit_action()

    def __set_timer(self) -> None:
        self.__timer.setRange(0, 5)
        self.__timer.setDecimals(2)
        self.__timer.setSingleStep(0.05)
        self.__timer.setSuffix(' sec')
        self.__timer.setFixedSize(80, 20)
        self.__timer.setLineEdit(QLineEdit())

    def __set_widgets(self) -> None:
        self.__set_timer()

    def __set_file_menu(self) -> None:
        self.__file_menu.setTitle('&File')
        self.__file_menu.addAction(self.__save_program_action)
        self.__file_menu.addAction(self.__save_tests_action)
        self.__file_menu.addAction(self.__save_all_action)
        self.__file_menu.addSeparator()
        self.__file_menu.addAction(self.__load_program_action)
        self.__file_menu.addAction(self.__load_tests_action)
        self.__file_menu.addSeparator()
        self.__file_menu.addAction(self.__exit_action)

    def __set_execution_menu(self) -> None:
        self.__execution_menu.setTitle('&Execution')
        self.__execution_menu.addAction(self.__run_action)
        self.__execution_menu.addAction(self.__debug_action)
        self.__execution_menu.addAction(self.__pause_action)
        self.__execution_menu.addAction(self.__stop_action)

    def __set_menu_bar(self) -> None:
        self.__set_file_menu()
        self.__set_execution_menu()
        # TODO: добавить остальные вкладки

    def __set_toolbar(self) -> None:
        self.__set_timer()
        # TODO: понять почему левый и верхний ContentMargin не работают (нижний и правый работают)
        # ^ на всякий случай можно поставить спейсер, наверно
        self.__toolbar.setMovable(False)
        self.__toolbar.addAction(self.__run_action)
        self.__toolbar.addAction(self.__debug_action)
        self.__toolbar.addAction(self.__pause_action)
        self.__toolbar.addAction(self.__stop_action)
        self.__toolbar.addSeparator()
        self.__toolbar.addAction(self.__save_program_action)
        self.__toolbar.addAction(self.__save_tests_action)
        self.__toolbar.addAction(self.__save_all_action)
        self.__toolbar.addSeparator()
        self.__toolbar.addAction(self.__load_program_action)
        self.__toolbar.addAction(self.__load_tests_action)
        self.__toolbar.addSeparator()
        self.__toolbar.addAction(self.__clear_tape_action)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.__toolbar.addWidget(spacer)
        self.__toolbar.addWidget(QLabel('Speed: '))
        self.__toolbar.addWidget(self.__timer)
        self.__toolbar.setContentsMargins(0, 0, 5, 0)  # TODO: нормально подравнять нужно
        self.addToolBar(Qt.TopToolBarArea, self.__toolbar)

    def __set_status_bar(self) -> None:
        self.statusBar().setStyleSheet('QStatusBar::item {border: None;}')
        self.statusBar().addWidget(self.__status_bar_icon)
        self.statusBar().addWidget(self.__status_bar_label)

    def __set_h_splitter(self) -> None:
        self.__h_splitter.addWidget(self.__table)
        self.__h_splitter.addWidget(self.__tape_list)
        self.__h_splitter.setStretchFactor(1, 0)
        self.__h_splitter.setSizes([800, 100])  # TODO: убрать хардкод

    def __set_v_splitter(self) -> None:
        self.__v_splitter.addWidget(self.__comment)
        self.__v_splitter.addWidget(self.__h_splitter)
        self.__v_splitter.setStretchFactor(0, 1)
        self.__v_splitter.setSizes([50, 450])  # TODO: убрать хардкод

    def __set_interface(self) -> None:
        self.__set_h_splitter()
        self.__set_v_splitter()
        self.__main_layout.addWidget(self.__v_splitter)
        self.__main_layout.addWidget(self.__tape)
        self.__main_layout.addWidget(self.__main_widget, 0, 0)

    def __enable_interface(self) -> None:
        ...
        # self.__run_action.setEnabled(True)
        # self.__pause_action.setEnabled(False)
        # self.__stop_action.setEnabled(False)
        # self.__table.setEnabled(True)
        # self.__tape_list.setEnabled(True)
        # self.__tape.setEnabled(True)

    def __disable_interface(self) -> None:
        ...
        # self.__run_action.setEnabled(False)
        # self.__pause_action.setEnabled(True)
        # self.__stop_action.setEnabled(True)
        # self.__table.setEnabled(False)
        # self.__tape_list.setEnabled(False)
        # self.__tape.setEnabled(False)

    def run_program(self):
        # self.__disable_interface()
        self.__program.set_mode(False)
        self.__program.start()

    def debug_program(self):
        # self.__disable_interface()
        self.__program.set_mode(True)
        self.__program.start()

    def pause_program(self):
        self.__program.pause()

    def stop_program(self):
        # self.__enable_interface()
        self.__program.stop()
        self.__program.quit()
        self.__program.wait()

    def clear_tape(self):
        self.__tape.reset()

    def init_ui(self):
        self.setGeometry(self.__x, self.__y, self.__width, self.__height)
        self.setWindowTitle('Post Machine')

        self.__set_actions()
        self.__set_widgets()
        self.__set_menu_bar()
        self.__set_toolbar()
        self.__set_status_bar()
        self.__set_interface()
        self.__enable_interface()

        self.setCentralWidget(self.__main_widget)
        self.show()
        self.log('Application loaded')

    def log(self, message: str, success: bool = True) -> None:
        self.__status_bar_icon.setPixmap(self.__OK if success else self.__ERROR)
        self.__status_bar_label.setText(message)

    def eventFilter(self, obj, event):
        # TODO: хочу, чтоб окно становилось меньше, когда от фулскрина переходишь к обычному размеру окна
        # if event.type() == QEvent.WindowStateChange:
        #     if int(self.windowState()) == Qt.WindowNoState:
        #         self.__tape.resize(self.__width)
        #         self.resize(self.__width, self.__height)
        if event.type() == QEvent.Resize:
            self.__tape.resize_width(self.size().width())
        return super().eventFilter(obj, event)

    def closeEvent(self, a0: QCloseEvent) -> None:
        if self.__saver.has_unsaved_data():
            message = QMessageBox()
            message.setWindowTitle('Unsaved changes')
            message.setText('Want to save your changes?')
            message.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            answer = message.exec()
            if answer == QMessageBox.Yes:
                if self.__saver.has_unsaved_program_data():
                    self.__saver.save_program()
                if self.__saver.has_unsaved_tests_data():
                    self.__saver.save_tests()
        else:
            answer = QMessageBox.Yes
        if answer == QMessageBox.Cancel:
            a0.ignore()
        else:
            a0.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    App = App()
    sys.exit(app.exec_())
