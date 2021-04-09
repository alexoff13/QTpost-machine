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
                    # TODO добавить: если стейт пустой, то просто переход на следующую строку
                    i = self.commands[self.app.table_program.table.item(i, 0).text()](
                        self.app.table_program.table.item(i, 1).text())
                    # TODO вставить в sleep значение крутилки
                    # sleep()
                except KeyError:
                    break
            else:
                sleep(0.0001)

    def set_a_label(self, to_state: str) -> int:
        self.app.signal_mark_carriage.emit()
        return int(to_state) - 1

    def reset_a_label(self, to_state: str) -> int:
        self.app.signal_unmark_carriage.emit()
        return int(to_state) - 1

    def go_to_right(self, to_state: str) -> int:
        self.app.signal_go_right.emit()
        return int(to_state) - 1

    def go_to_left(self, to_state: str) -> int:
        self.app.signal_go_left.emit()
        return int(to_state) - 1

    def select_a_state(self, app, states: str):
        state1, state2 = states.split()
        self.complete_event = True
        return int(state2) - 1 if app.tape.is_carriage_marked() else int(state1) - 1

    @staticmethod
    def exit_(to_state: str) -> int:
        return -1
