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
        path = QFileDialog.getSaveFileName(self.__parent, self.CHOOSE_FILE, file_name)[0]
        return None if path == '' else path

    def __save_program(self) -> bool:
        data = self.get_program_data()
        try:
            with open(self.__program_path, 'w') as fout:
                json.dump(data, fout, indent=2)
            self.__program_data = data
            self.__parent.log('The program was saved successfully', True)
            return True
        except TypeError:
            self.__parent.log('Failed to save the program', False)
            return False

    def __save_tests(self) -> bool:
        data = self.get_tests_data()
        try:
            with open(self.__tests_path, 'w') as fout:
                json.dump(data, fout, indent=2)
            self.__tests_data = data
            self.__parent.log('The tests were saved successfully', True)
            return True
        except TypeError:
            self.__parent.log('Failed to save the tests', False)
            return False

    def save_program(self) -> bool:
        if self.__program_path is None:
            return self.save_program_as()
        else:
            return self.__save_program()

    def save_program_as(self) -> bool:
        self.__program_path = self.__get_file_path(self.PROGRAM_NAME)
        return self.__save_program()

    def get_program_data(self) -> dict:
        program_data = {
            'comment': self.__comment.get_data(),
            'table': self.__table.get_data(),
            'tape': self.__tape_list.get_main_data()
        }
        return program_data

    def save_tests(self) -> bool:
        if self.__tests_path is None:
            return self.save_tests_as()
        else:
            return self.__save_tests()

    def save_tests_as(self) -> bool:
        self.__tests_path = self.__get_file_path(self.TESTS_NAME)
        return self.__save_tests()

    def get_tests_data(self) -> dict:
        tests_data = self.__tape_list.get_tests_data()
        return tests_data

    def save_all(self):
        is_program_saved = self.save_program()
        are_tests_saved = self.save_tests()
        if is_program_saved and are_tests_saved:
            self.__parent.log('The program and the tests were saved successfully', True)
        elif is_program_saved and not are_tests_saved:
            self.__parent.log('Only the program was saved successfully', False)
        elif not is_program_saved and are_tests_saved:
            self.__parent.log('Only the tests were saved successfully', False)
        else:
            self.__parent.log('Failed to save the program and the tests', False)

    def has_unsaved_program_data(self) -> bool:
        return self.__comment.has_unsaved_data() or self.__table.has_unsaved_data() or \
               self.__tape_list.has_main_unsaved_data()

    def has_unsaved_tests_data(self) -> bool:
        return self.__tape_list.has_tests_unsaved_data()

    def has_unsaved_data(self) -> bool:
        return self.is_program_unsaved() or self.are_tests_unsaved()

    def is_program_unsaved(self) -> bool:
        return self.has_unsaved_program_data() and self.__program_data != self.get_program_data()

    def are_tests_unsaved(self) -> bool:
        return self.has_unsaved_tests_data() and self.__tests_data != self.get_tests_data()

    def update_program_data(self) -> None:
        self.__program_data = self.get_program_data()

    def update_tests_data(self) -> None:
        self.__tests_data = self.get_tests_data()
