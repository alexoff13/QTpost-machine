from time import sleep

from PyQt5.QtCore import QThread, QRunnable, pyqtBoundSignal
from PyQt5.QtWidgets import QDoubleSpinBox

from utils.signals import RunnerSignals
from widgets.table import Table
from widgets.tape import Tape


class Runner(QRunnable):
    __signals = RunnerSignals()

    def __init__(self, table: Table, tape: Tape, timer: QDoubleSpinBox):
        super().__init__()
        self.__table = table
        self.__tape = tape
        self.__timer = timer
        self.__is_running = False
        self.__is_event_completed = False
        self.__set_signals()
        self.__commands = {
            '+': self.__mark_carriage,
            'x': self.__unmark_carriage,
            '>': self.__go_right,
            '<': self.__go_left,
            '?': self.__select_a_state,
            '!': self.__end
        }

    def __set_signals(self) -> None:
        self.__signals.go_right.connect(self.__tape.go_right)
        self.__signals.go_left.connect(self.__tape.go_left)
        self.__signals.mark_carriage.connect(self.__tape.mark_carriage)
        self.__signals.unmark_carriage.connect(self.__tape.unmark_carriage)
        self.__signals.update.connect(self.update)

    # такой странный слип, чтобы, например, при переходе таймера с 5 на 0.01, сразу же происходили изменения
    def __pause(self) -> None:
        time_spent = 0
        while time_spent < self.__timer.value():
            sleep(0.01)
            time_spent += 0.01

    def __mark_carriage(self, to_state: str) -> int:
        self.__signals.mark_carriage.emit(self.__signals.update)
        return int(to_state) - 1

    def __unmark_carriage(self, to_state: str) -> int:
        self.__signals.unmark_carriage.emit(self.__signals.update)
        return int(to_state) - 1

    def __go_right(self, to_state: str) -> int:
        self.__signals.go_right.emit(self.__signals.update)
        return int(to_state) - 1

    def __go_left(self, to_state: str) -> int:
        self.__signals.go_left.emit(self.__signals.update)
        return int(to_state) - 1

    def __select_a_state(self, states: str):
        state1, state2 = states.split()
        line = (int(state2) if self.__tape.is_carriage_marked() else int(state1)) - 1
        self.update()
        return line

    def __end(self, to_state: str) -> int:
        self.stop()
        return -1

    def run(self):
        commands = self.__table.get_data()
        self.__is_event_completed = True
        self.__is_running = True
        line = 0
        while self.__is_running:
            if self.__is_event_completed:
                self.__is_event_completed = False
                # self.__signals.go_right.emit(self.__signals.update)
                # TODO добавить: если стейт пустой, то просто переход на следующую строку
                line = self.__commands[commands[line][0]](commands[line][1])
                self.__pause()
            else:
                sleep(0.00001)

    def stop(self) -> None:
        self.__is_running = False

    def update(self):
        self.__is_event_completed = True


class Program(QThread):
    def __init__(self, table: Table, tape: Tape, timer: QDoubleSpinBox, on_stop: pyqtBoundSignal = None) -> None:
        super().__init__()
        self.__table = table
        self.__tape = tape
        self.__timer = timer
        self.__runner = Runner(self.__table, self.__tape, self.__timer)
        self.__on_stop_signal = on_stop

    def run(self) -> None:
        try:
            self.__runner.run()
        except KeyError:
            # В программе что-то пошло не так
            if self.__on_stop_signal is not None:
                self.__on_stop_signal.emit()

    def stop(self) -> None:
        self.__runner.stop()
