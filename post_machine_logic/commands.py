from time import sleep

from PyQt5.QtCore import QThread, pyqtBoundSignal
from PyQt5.QtWidgets import QDoubleSpinBox

from utils.signals import RunnerSignals
from widgets.table import Table
from widgets.tape import Tape


class Runner():
    _signals = RunnerSignals()

    def __init__(self, table: Table, tape: Tape, timer: QDoubleSpinBox):
        # super().__init__()
        self._table = table
        self._tape = tape
        self._timer = timer
        self._is_running = False
        self._is_event_completed = False
        self._set_signals()
        self._commands = {
            '+': self._mark_carriage,
            'x': self._unmark_carriage,
            '>': self._go_right,
            '<': self._go_left,
            '?': self._select_a_state,
            '!': self._end
        }
        # поля для дебаггера, прошу не трогать!!!!!!!!!!!!!!!!!
        self._is_event_completed = True
        self._is_running = True
        self._pause_run_program = False
        self.line = 0

    def _set_signals(self) -> None:
        self._signals.go_right.connect(self._tape.go_right)
        self._signals.go_left.connect(self._tape.go_left)
        self._signals.mark_carriage.connect(self._tape.mark_carriage)
        self._signals.unmark_carriage.connect(self._tape.unmark_carriage)
        self._signals.update.connect(self.update)

    # такой странный слип, чтобы, например, при переходе таймера с 5 на 0.01, сразу же происходили изменения
    def _pause(self) -> None:
        time_spent = 0
        while time_spent < self._timer.value():
            sleep(0.01)
            time_spent += 0.01

    def _mark_carriage(self, to_state: str) -> int:
        self._signals.mark_carriage.emit(self._signals.update)
        return int(to_state) - 1

    def _unmark_carriage(self, to_state: str) -> int:
        self._signals.unmark_carriage.emit(self._signals.update)
        return int(to_state) - 1

    def _go_right(self, to_state: str) -> int:
        self._signals.go_right.emit(self._signals.update)
        return int(to_state) - 1

    def _go_left(self, to_state: str) -> int:
        self._signals.go_left.emit(self._signals.update)
        return int(to_state) - 1

    def _select_a_state(self, states: str):
        state1, state2 = states.split()
        line = (int(state2) if self._tape.is_carriage_marked() else int(state1)) - 1
        self.update()
        return line

    def _end(self, to_state: str) -> int:
        self.stop()
        return -1

    def debug(self):
        self._is_running = True
        self.commands = self._table.get_data()
        if self._is_running and self._is_event_completed:
            self._is_event_completed = False
            # self.__signals.go_right.emit(self.__signals.update)
            # TODO добавить: если стейт пустой, то просто переход на следующую строку
            self.line = self._commands[self.commands[self.line][0]](self.commands[self.line][1])
            self._pause()

    def run(self):
        commands = self._table.get_data()
        self._is_event_completed = True
        self._is_running = True
        line = 0
        while self._is_running:
            if self._is_event_completed and not self._pause_run_program:
                self._is_event_completed = False
                # self.__signals.go_right.emit(self.__signals.update)
                # TODO добавить: если стейт пустой, то просто переход на следующую строку
                line = self._commands[commands[line][0]](commands[line][1])
                self._pause()
            else:
                sleep(0.00001)

    def pause_run(self):
        self._pause_run_program = not self._pause_run_program

    def stop(self) -> None:
        self._is_running = False

    def update(self):
        self._is_event_completed = True


class Program(QThread):
    def __init__(self, table: Table, tape: Tape, timer: QDoubleSpinBox,
                 on_stop: pyqtBoundSignal = None) -> None:
        super().__init__()
        self.__table = table
        self.__tape = tape
        self.__timer = timer
        self.__is_debug = False
        self.__runner = Runner(self.__table, self.__tape, self.__timer)
        self.__on_stop_signal = on_stop

    def __select_mode(self):
        if self.__is_debug:
            return self.__runner.debug
        else:
            return self.__runner.run

    def set_mode(self, is_debug: bool):
        self.__is_debug = is_debug

    def run(self) -> None:
        try:
            self.__select_mode()()
        except KeyError:
            # В программе что-то пошло не так
            if self.__on_stop_signal is not None:
                self.__on_stop_signal.emit()

    def pause(self):
        self.__runner.pause_run()

    def stop(self) -> None:
        self.__runner.stop()
