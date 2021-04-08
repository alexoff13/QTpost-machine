from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal

# from main import App
from utils import Saver

# ToDO реализовать вопрос
class Runner(QThread):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.commands = {
            '+': self.set_a_label,
            'x': self.reset_a_label,
            '>': self.go_to_right,
            '<': self.go_to_left,
            '?': self.func,
            '!': self.exit_,
        }

    @staticmethod
    def func(str1):
        pass

    def __del__(self):
        self.wait()

    def run(self):
        self.program = Saver.save_program_to_dict(self.app)
        i = 0
        while i != -1:
            sleep(0.1)
            print(i)
            try:
                i = self.commands[self.app.table_program.table.item(i, 0).text()](
                    self.app, self.app.table_program.table.item(i, 1).text())
            except:
                break


    @staticmethod
    def set_a_label(app, to_state: str) -> int:
        app.Signal_inverse_carriage.emit()
        return int(to_state) - 1

    @staticmethod
    def reset_a_label(app, to_state: str) -> int:
        app.Signal_inverse_carriage_false.emit()
        return int(to_state) - 1

    @staticmethod
    def go_to_right(app, to_state: str) -> int:
        app.Signal_go_right.emit()
        return int(to_state) - 1

    @staticmethod
    def go_to_left(app, to_state: str) -> int:
        app.Signal_go_left.emit()
        return int(to_state) - 1

    @staticmethod
    def exit_(app, to_state: str) -> int:
        return -1
