from time import sleep

from PyQt5.QtCore import QThread


class Runner(QThread):

    def __init__(self, app, program: dict, timer):
        super().__init__()
        self.program = program
        self.sleep_time = timer
        self.app = app
        self.commands = {
            '+': self.set_a_label,
            'x': self.reset_a_label,
            '>': self.go_to_right,
            '<': self.go_to_left,
            '?': self.select_a_state,
            '!': self.exit_
        }
        self.stop_program = False
        self.complete_event = True

    def __del__(self):
        self.wait()

    # TODO: лента и программа должны стать неактивными во время выполнения программы
    def run(self):
        self.stop_program = False
        table = self.program['program']
        i = 0
        while i != -1:
            if self.complete_event:
                self.complete_event = False
                try:
                    i = self.commands[table[i][0]](table[i][1])
                    sleep(self.sleep_time.value())
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
        res = (int(state2) if self.app.return_state_carriage() else int(state1)) - 1
        self.complete_event = True
        return res

    def exit_(self, to_state: str) -> int:
        self.complete_event = True
        return -1

    def set_sleep_time(self, sleep_time: float) -> None:
        self.sleep_time = sleep_time
