from time import sleep

from PyQt5.QtCore import QThread, pyqtBoundSignal

from utils.signals import RunnerSignals
from widgets.table import Table
from widgets.tape import Tape
from widgets.timer import Timer


class Runner:
    _signals = RunnerSignals()

    def __init__(self, table: Table, tape: Tape, timer: Timer, on_stop: pyqtBoundSignal):
        # super().__init__()
        self._table = table
        self._tape = tape
        self._timer = timer
        self._on_stop = on_stop
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
        self.commands = dict()
        self._is_event_completed = True
        self._is_running = True
        self._pause_run_program = False
        self.__line = 0

    @property
    def line(self):
        return self.__line

    def _set_signals(self) -> None:
        self._signals.go_right.connect(self._tape.go_right)
        self._signals.go_left.connect(self._tape.go_left)
        self._signals.mark_carriage.connect(self._tape.mark_carriage)
        self._signals.unmark_carriage.connect(self._tape.unmark_carriage)
        self._signals.select_row_in_table.connect(self._table.set_selected_line)
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
        try:
            state1, state2 = states.split()
        except ValueError:
            state1, or_, state2 = states.split()
        line = (int(state2) if self._tape.is_carriage_marked() else int(state1)) - 1
        self.update()
        return line

    def _end(self, to_state: str = None) -> int:
        self.stop()
        self._on_stop.emit()
        self._is_event_completed = True
        self.__select_line(-1)
        return 0

    def debug(self):
        self._is_running = True
        commands = self._table.get_data()
        if self._is_running and self._is_event_completed:
            self.__select_line()
            self._is_event_completed = False
            self.__line = self._commands[commands[self.__line][0]](commands[self.__line][1])

    def run(self):
        commands = self._table.get_data()
        self._is_event_completed = True
        self._is_running = True

        while self._is_running:
            if self._is_event_completed and not self._pause_run_program:
                self.__select_line()
                self._is_event_completed = False
                # TODO некст стейт если пустой
                # try:
                #     next_state = int(commands[self.__line][1])
                # except ValueError:
                #     next_state = self.__line + 2
                # try:
                #     self.__line = self._commands[commands[self.__line][0]](next_state)
                # except KeyError:
                #     self._end()
                self.__line = self._commands[commands[self.__line][0]](commands[self.__line][1])
                self._pause()
            else:
                sleep(0.00001)

    def __select_line(self, value: int = -2):
        if value == -2:
            self._table.set_current_line_in_run(self.line)
        else:
            self._table.set_current_line_in_run(-1)
        self._signals.select_row_in_table.emit(self._signals.update)

    def pause_run(self):
        self._pause_run_program = not self._pause_run_program

    @property
    def pause_run_program(self) -> bool:
        return self._pause_run_program

    def stop(self) -> None:
        self._pause_run_program = False
        self.__line = 0
        self._is_running = False

    def update(self):
        self._is_event_completed = True


class Program(QThread):
    def __init__(self, table: Table, tape: Tape, timer: Timer, on_stop: pyqtBoundSignal = None) -> None:
        super().__init__()
        self.__table = table
        self.__tape = tape
        self.__timer = timer
        self.__is_debug = False
        self.__runner = Runner(self.__table, self.__tape, self.__timer, on_stop)
        self.__on_stop = on_stop

    def __select_mode(self):
        if self.__is_debug:
            return self.__runner.debug
        else:
            return self.__runner.run

    def set_mode(self, is_debug: bool):
        self.__is_debug = is_debug

    def debug(self) -> None:
        self.__runner.debug()

    def run(self) -> None:
        try:
            self.__select_mode()()
        except KeyError:
            # В программе что-то пошло не так
            if self.__on_stop is not None:
                self.__runner.stop()
                self.__on_stop.emit()

    def is_paused(self) -> bool:
        return self.__runner.pause_run_program

    def pause(self):
        self.__runner.pause_run()

    def stop(self) -> None:
        self.__runner.stop()
