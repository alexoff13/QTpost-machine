from PyQt5 import QtCore
from PyQt5.QtCore import QObject


class RunnerSignals(QObject):
    go_right = QtCore.pyqtSignal(QtCore.pyqtBoundSignal)
    go_left = QtCore.pyqtSignal(QtCore.pyqtBoundSignal)
    mark_carriage = QtCore.pyqtSignal(QtCore.pyqtBoundSignal)
    unmark_carriage = QtCore.pyqtSignal(QtCore.pyqtBoundSignal)
    select_row_in_table = QtCore.pyqtSignal(QtCore.pyqtBoundSignal)
    update = QtCore.pyqtSignal()


class ProgramSignals(QObject):
    on_stop = QtCore.pyqtSignal()


class TapeSignals(QObject):
    to_left = QtCore.pyqtSignal()
    to_right = QtCore.pyqtSignal()


class MainSignals(QObject):
    active_reset = QtCore.pyqtSignal()
    inactive_reset = QtCore.pyqtSignal()
