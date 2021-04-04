import json

from tape import Tape


class Loader:
    @staticmethod
    def load_program(app):
        with open('test.pmp', mode='r') as fin:
            program = json.load(fin)
        tape_data = program['tape']
        program_data = program['program']

        app.tape.set_from_file(tape_data)
        app.table_program.set_from_file(program_data)

