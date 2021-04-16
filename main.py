import sys

from PyQt5.QtCore import Qt, QEvent, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QDoubleSpinBox, QMainWindow, QAction,
                             QToolBar, QGridLayout, QSizePolicy, QSplitter, QLabel)

from comment import Comment
from post_machine_logic import Runner
from table import Table
from tape_list import TapeList
from tape import Tape
from utils import Loader
from utils import Saver


# TODO: во время (не) выполнения программы некоторые элементы должны быть не активными


class App(QMainWindow):

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
        self.__stop_action = QAction()
        self.__debug_action = QAction()
        self.__save_action = QAction()
        self.__load_action = QAction()
        self.__reset_action = QAction()
        self.__exit_action = QAction()
        self.__timer = QDoubleSpinBox()
        # инициализация меню
        self.__menu_bar = self.menuBar()
        self.__file_menu = self.__menu_bar.addMenu(str())
        # TODO: добавить ещё нужные меню
        # инициализация тулбара
        self.__toolbar: QToolBar
        # инициализация основых элементов экрана
        # TODO: исправить баг со сплиттером - при чрезмерном сдвиге в сторону, виджет в той же стороне исчезает
        # ^ хотя его можно вернуть - может быть это просто фича такая?
        self.__h_splitter = QSplitter(Qt.Horizontal)  # горизонтальный сплиттер
        self.__v_splitter = QSplitter(Qt.Vertical)  # вертикальный сплиттер
        self.__comment = Comment()
        self.__table = Table()
        self.__tape_list = TapeList()
        self.__tape = Tape(self.__width)
        # инициализация сигналов
        self.__signal_mark_carriage = pyqtSignal()
        self.__signal_unmark_carriage = pyqtSignal()
        self.__signal_go_right = pyqtSignal()
        self.__signal_go_left = pyqtSignal()
        # инициализация раннера, сейвера и загрузчика
        # TODO: пипец там инкапсуляции ноль, поэтому всё ломается мгновенно при создании раннера
        # self.runner = Runner(self)
        # установка получения событий
        self.installEventFilter(self)
        # инициализация пользовательского интерфейса
        self.init_ui()

    def __set_signals(self) -> None:
        self.__signal_mark_carriage.connect(self.__tape.mark_carriage)
        self.__signal_unmark_carriage.connect(self.__tape.unmark_carriage)
        self.__signal_go_right.connect(self.__tape.go_right)
        self.__signal_go_left.connect(self.__tape.go_left)

    def __set_run_action(self) -> None:
        self.__run_action.setIcon(QIcon('icons/run-button.png'))
        self.__run_action.setText('Run')
        self.__run_action.setShortcut('Ctrl+R')
        self.__run_action.setStatusTip('Run program')
        self.__run_action.triggered.connect(self.run_program)

    def __set_stop_action(self) -> None:
        self.__stop_action.setIcon(QIcon('icons/stop-button.png'))
        self.__stop_action.setText('Stop')
        self.__stop_action.setShortcut('Ctrl+Alt+S')
        self.__stop_action.setStatusTip('Stop program')
        self.__stop_action.triggered.connect(self.stop_program)

    def __set_exit_action(self) -> None:
        self.__exit_action.setIcon(QIcon(''))
        self.__exit_action.setText('Exit')
        self.__exit_action.setShortcut('Ctrl+E')
        self.__exit_action.setStatusTip('Exit application')
        self.__exit_action.triggered.connect(self.close)

    def __set_actions(self) -> None:
        self.__set_run_action()
        self.__set_stop_action()
        # TODO: добавить остальные действия
        self.__set_exit_action()

    def __set_timer(self) -> None:
        self.__timer.setRange(0.05, 1)
        self.__timer.setDecimals(2)
        self.__timer.setSingleStep(0.05)
        self.__timer.setSuffix(' sec')
        self.__timer.setFixedSize(80, 20)

    def __set_widgets(self) -> None:
        self.__set_timer()

    def __set_file_menu(self) -> None:
        self.__file_menu.setTitle('&File')
        self.__file_menu.addAction(self.__run_action)
        self.__file_menu.addAction(self.__stop_action)
        self.__file_menu.addSeparator()
        self.__file_menu.addAction(self.__exit_action)

    def __set_menu_bar(self) -> None:
        self.__set_file_menu()
        # TODO: добавить остальные вкладки

    def __set_toolbar(self) -> None:
        self.__set_timer()
        # TODO: понять почему левый и верхний ContentMargin не работают (нижний и правый работают)
        # ^ на всякий случай можно поставить спейсер, наверно
        self.__toolbar = QToolBar()
        self.__toolbar.setMovable(False)
        self.__toolbar.addAction(self.__run_action)
        self.__toolbar.addAction(self.__stop_action)
        # TODO: добавить остальные кнопки
        self.__toolbar.addSeparator()
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.__toolbar.addWidget(spacer)
        self.__toolbar.addWidget(QLabel('Speed: '))
        self.__toolbar.addWidget(self.__timer)
        self.__toolbar.setContentsMargins(0, 0, 5, 0)  # TODO: нормально подравнять нужно
        self.addToolBar(Qt.TopToolBarArea, self.__toolbar)

    def __set_status_bar(self) -> None:
        # для изменения, например, шрифта или положения статусбара
        pass

    def __set_h_splitter(self) -> None:
        self.__h_splitter.addWidget(self.__table)
        self.__h_splitter.addWidget(self.__tape_list)
        self.__h_splitter.setStretchFactor(1, 0)
        self.__h_splitter.setSizes([750, 150])  # TODO: убрать хардкод

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

    def init_ui(self):
        self.setGeometry(self.__x, self.__y, self.__width, self.__height)
        self.setWindowTitle('Post Machine')

        self.__set_actions()
        self.__set_widgets()
        self.__set_menu_bar()
        self.__set_toolbar()
        self.__set_status_bar()
        self.__set_interface()

        self.setCentralWidget(self.__main_widget)
        self.show()
        self.log('Application loaded')

    def log(self, message: str) -> None:
        self.statusBar().showMessage(message)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Resize:
            self.__tape.resize(self.size().width())
        return super().eventFilter(obj, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    App = App()
    sys.exit(app.exec_())
