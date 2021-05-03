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

    def __init__(self, parent: any, comment: Comment, table: Table, tape: Tape, tape_list: TapeList) -> None:
        self.__parent = parent
        self.__comment = comment
        self.__table = table
        self.__tape = tape
        self.__tape_list = tape_list
        self.__program_data = None
        self.__tests_data = None
        self.__program_path = None
        self.__tests_path = None

    def __get_file_path(self, file_name: str) -> str:
        path = QFileDialog.getOpenFileName(self.__parent, self.CHOOSE_FILE, file_name)[0]
        return None if path == '' else path

    def __save_program(self) -> None:
        data = self.get_program_data()
        try:
            with open(self.__program_path, 'w') as fout:
                json.dump(data, fout, indent=2)
            self.__program_data = data
        except TypeError:
            pass

    def __save_tests(self) -> None:
        data = self.get_tests_data()
        try:
            with open(self.__tests_path, 'w') as fout:
                json.dump(data, fout, indent=2)
            self.__tests_data = data
        except TypeError:
            pass

    def save_program(self):
        if self.__program_path is None:
            self.save_program_as()
        else:
            self.__save_program()

    def save_program_as(self):
        self.__program_path = self.__get_file_path(self.PROGRAM_NAME)
        self.__save_program()

    def get_program_data(self) -> dict:
        program_data = {
            'comment': self.__comment.get_data(),
            'table': self.__table.get_data(),
            'tape': self.__tape.get_data()
        }
        return program_data

    def save_tests(self):
        if self.__tests_path is None:
            self.save_tests_as()
        else:
            self.__save_tests()

    def save_tests_as(self):
        self.__tests_path = self.__get_file_path(self.TESTS_NAME)
        self.__save_tests()

    def get_tests_data(self) -> dict:
        tests_data = self.__tape_list.get_data()
        return tests_data

    def save_all(self):
        self.save_program()
        self.save_tests()

    def is_program_unsaved(self) -> bool:
        return self.__program_data != self.get_program_data()

    def are_tests_unsaved(self) -> bool:
        return self.__tests_data != self.get_tests_data()
