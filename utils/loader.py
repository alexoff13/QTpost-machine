import json
from json import JSONDecodeError

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from utils import Saver
from widgets.comment import Comment
from widgets.table import Table
from widgets.tape import Tape
from widgets.tape_list import TapeList


class LoadCancel(Exception):
    pass


class Loader:
    OPEN_FILE = 'Open file'
    DEFAULT_DIRECTORY = './~'

    def __init__(self, parent: any, comment: Comment, table: Table, tape: Tape, tape_list: TapeList,
                 saver: Saver) -> None:
        self.__parent = parent
        self.__comment = comment
        self.__table = table
        self.__tape = tape
        self.__tape_list = tape_list
        self.__saver = saver

    def __get_file_path(self) -> str:
        return QFileDialog.getOpenFileName(self.__parent, self.OPEN_FILE, self.DEFAULT_DIRECTORY)[0]

    @staticmethod
    def unsaved_data_message(on_yes) -> None:
        message = QMessageBox()
        message.setIcon(QMessageBox.Question)
        message.setWindowTitle('Unsaved changes')
        message.setText('Want to save your changes?')
        message.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        answer = message.exec()
        if answer == QMessageBox.Yes:
            on_yes()
        elif answer == QMessageBox.Cancel:
            raise LoadCancel

    def __unsaved_program_warning(self) -> None:
        if self.__saver.is_program_unsaved():
            self.unsaved_data_message(self.__saver.save_program)

    def __unsaved_tests_warning(self) -> None:
        if self.__saver.are_tests_unsaved():
            self.unsaved_data_message(self.__saver.save_tests)

    def open_program(self) -> None:
        try:
            self.__unsaved_program_warning()
            path = self.__get_file_path()
            with open(path, 'r') as fin:
                program = json.load(fin)
            self.__comment.set_from_file(program['comment'])
            self.__table.set_from_file(program['table'])
            self.__tape_list.set_main_from_file(program['main'])
            self.__saver.update_program_data()
            self.__saver.set_program_path(path)
            self.__parent.log('The program has been successfully opened', True)
        except (KeyError, JSONDecodeError):
            self.__parent.log('Wrong program file selected or the program file is damaged', False)
        except (FileNotFoundError, LoadCancel):  # ?????????? ???????????????????? ??????????-???????? ????????????
            self.__parent.log('Failed to open the program', False)

    def open_tests(self) -> None:
        try:
            self.__unsaved_tests_warning()
            path = self.__get_file_path()
            with open(path, 'r') as fin:
                tests = json.load(fin)
            self.__tape_list.set_tests_from_file(tests)
            self.__saver.update_tests_data()
            self.__saver.set_tests_path(path)
            self.__parent.log('The tests have been successfully opened', True)
        except (KeyError, JSONDecodeError):
            self.__parent.log('Wrong tests file selected or the tests file is damaged', False)
        except (FileNotFoundError, LoadCancel):  # ?????????? ???????????????????? ??????????-???????? ????????????
            self.__parent.log('Failed to open the tests', False)
