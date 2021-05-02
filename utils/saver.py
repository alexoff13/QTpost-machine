import json

from PyQt5.QtWidgets import QFileDialog

from widgets.comment import Comment
from widgets.table import Table
from widgets.tape import Tape
from widgets.tape_list import TapeList


class Saver:
    CHOOSE_FILE = 'Choose file'
    PROGRAM_NAME = './program.pmp'
    TESTS_NAME = './tests.pmt'

    def __init__(self, parent: any, comment: Comment, table: Table, tape: Tape, tape_list: TapeList):
        self.__parent = parent
        self.__comment = comment
        self.__table = table
        self.__tape = tape
        self.__tape_list = tape_list
        self.__program_path = None
        self.__tests_path = None

    def save_program(self):
        if self.__program_path is None:
            self.save_program_as()
        else:
            self.__save_program()

    def save_program_as(self):
        self.__program_path = QFileDialog.getSaveFileName(self.__parent, self.CHOOSE_FILE, self.PROGRAM_NAME)[0]
        self.__save_program()

    def get_program_data(self) -> dict:
        program_data = {
            'comment': self.__comment.get_data(),
            'table': self.__table.get_data(),
            'tape': self.__tape.get_data()
        }
        return program_data

    def __save_program(self) -> None:
        program_data = self.get_program_data()
        with open(self.__program_path, 'w') as fout:
            json.dump(program_data, fout, indent=2)

    def save_tests(self):
        if self.__tests_path is None:
            self.save_tests_as()
        else:
            self.__save_tests()

    def save_tests_as(self):
        self.__program_path = QFileDialog.getSaveFileName(self.__parent, self.CHOOSE_FILE, self.TESTS_NAME)[0]
        self.__save_tests()

    def get_tests_data(self) -> dict:
        tests_data = self.__tape_list.get_data()
        return tests_data

    def __save_tests(self) -> None:
        tests_data = self.get_tests_data()
        with open(self.__tests_path, 'w') as fout:
            json.dump(tests_data, fout, indent=2)
