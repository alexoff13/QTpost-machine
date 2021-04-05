import json

from PyQt5.QtWidgets import QFileDialog

from tape import Tape


class Loader:
    @staticmethod
    def load_program(app):
        fname = QFileDialog.getOpenFileName(app, 'Open file', './~')[0]
        try:
            with open(fname, mode='r') as fin:
                program = json.load(fin)
        except:
            pass

        tape_data = program['tape']
        program_data = program['program']

        app.tape.set_from_file(tape_data)
        app.table_program.set_from_file(program_data)

