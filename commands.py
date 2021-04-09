from time import sleep

from PyQt5.QtCore import QThread

from utils import Saver




class Runner(QThread):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.commands = {
            '+': self.set_a_label,
            'x': self.reset_a_label,
            '>': self.go_to_right,
            '<': self.go_to_left,
            '?': self.select_a_state,
            '!': self.exit_,
        }
        self.program = Saver.save_program_to_dict(self.app)
        self.complete_event = True

    def __del__(self):
        self.wait()

    def run(self):
        self.program = Saver.save_program_to_dict(self.app)
        i = 0
        while i != -1:
            if self.complete_event:
                self.complete_event = False
                try:
                    i = self.commands[self.app.table_program.table.item(i, 0).text()](
                        self.app, self.app.table_program.table.item(i, 1).text())
                except KeyError:
                    break
            else:
                sleep(0.0001)

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

    def select_a_state(self, app, states: str):
        state1, state2 = states.split()
        self.complete_event = True
        return int(state2) - 1 if app.tape.is_carriage_marked() else int(state1) - 1

    @staticmethod
    def exit_(app, to_state: str) -> int:
        return -1
