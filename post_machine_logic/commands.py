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
            '!': self.exit_
        }
        self.program = Saver.save_program_to_dict(self.app)
        self.stop_program = False
        self.complete_event = True

    def __del__(self):
        self.wait()

    # TODO: лента и программа должны стать неактивными во время выполнения программы
    def run(self):
        self.stop_program = False
        self.program = Saver.save_program_to_dict(self.app)
        i = 0
        while i != -1:
            if self.complete_event:
                self.complete_event = False
                try:
                    # TODO добавить: если стейт пустой, то просто переход на следующую строку
                    i = self.commands[self.app.table_program.__column.item(i, 0).text()](self.app.table_program.__column.item(i, 1).text())
                    # TODO вставить в sleep значение крутилки
                    # sleep()
                except KeyError:
                    break
            else:
                sleep(0.0001)

            if self.stop_program:
                i = -1

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

    def select_a_state(self, states: str):
        state1, state2 = states.split()
        res = (int(state2) if self.app.__tape.is_carriage_marked() else int(state1)) - 1
        self.complete_event = True
        return res

    def exit_(self, to_state: str) -> int:
        self.complete_event = True
        return -1
