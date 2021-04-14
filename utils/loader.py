import json

from PyQt5.QtWidgets import QFileDialog


class Loader:
    @staticmethod
    def load_program(app):
        fname = QFileDialog.getOpenFileName(app, 'Open file', './~')[0]
        try:
            with open(fname, mode='r') as fin:
                program = json.load(fin)
        except:
            return
        Loader.load_program_from_dict(program, app)

    @staticmethod
    def load_program_from_dict(program, app):
        tape_data = program['tape']
        program_data = program['program']
        app.tape.reset()
        app.table_program.reset()
        app.tape.set_from_file(tape_data)
        app.table_program.set_from_file(program_data)
