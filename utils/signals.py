from PyQt5 import QtCore
from PyQt5.QtCore import QObject


class RunnerSignals(QObject):
    go_right = QtCore.pyqtSignal(QtCore.pyqtBoundSignal)
    go_left = QtCore.pyqtSignal(QtCore.pyqtBoundSignal)
    mark_carriage = QtCore.pyqtSignal(QtCore.pyqtBoundSignal)
    unmark_carriage = QtCore.pyqtSignal(QtCore.pyqtBoundSignal)
    update = QtCore.pyqtSignal()


class ProgramSignals(QObject):
    on_stop = QtCore.pyqtSignal()
