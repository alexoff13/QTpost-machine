import json

from PyQt5.QtWidgets import QFileDialog


class Saver():

    def __init__(self, parent):
        self.__parent = parent

    def save_program(self, tape_data, table_data):

        program = self.save_program_to_dict(tape_data, table_data)
        fname = QFileDialog.getSaveFileName(self.__parent, 'Choose file', './program.pmp')[0]
        try:
            with open(fname, mode='w') as fout:
                json.dump(program, fout, sort_keys=True, indent=4)
        except:
            pass

    @staticmethod
    def save_program_to_dict(tape_data, table_data):
        program = {
            'tape': tape_data,
            'program': table_data,
        }
        # todo перенести получение дикта в классы
        return program






