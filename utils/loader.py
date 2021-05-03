import json
from json import JSONDecodeError

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from utils import Saver
from widgets.comment import Comment
from widgets.table import Table
from widgets.tape import Tape
from widgets.tape_list import TapeList


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

    def __unsaved_program_warning(self) -> None:
        if self.__saver.is_program_unsaved() and self.get_answer():
            self.__saver.save_program()

    def __unsaved_tests_warning(self) -> None:
        if self.__saver.are_tests_unsaved() and self.get_answer():
            self.__saver.save_tests()

    def load_program(self) -> None:
        try:
            with open(self.__get_file_path(), 'r') as fin:
                program = json.load(fin)
            self.__comment.set_from_file(program['comment'])
            self.__table.set_from_file(program['table'])
            self.__tape.set_from_file(program['tape'])
        except (JSONDecodeError, KeyError):
            # TODO: код для посланания сообщения, что файл неверного формата
            pass
        except FileNotFoundError:
            pass

    def load_tests(self) -> None:
        try:
            self.__unsaved_tests_warning()
            with open(self.__get_file_path(), 'r') as fin:
                tests = json.load(fin)
            self.__tape_list.set_from_file(tests)
        except (JSONDecodeError, KeyError):
            # TODO: код для посланания сообщения, что файл неверного формата
            pass
        except FileNotFoundError:
            pass

    @staticmethod
    def get_answer() -> bool:
        message = QMessageBox()
        message.setWindowTitle('Unsaved changes')
        message.setText('Want to save your changes?')
        message.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        answer = message.exec()
        return answer == QMessageBox.Yes
