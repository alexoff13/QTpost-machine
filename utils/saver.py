import json

from PyQt5.QtWidgets import QFileDialog


class Saver:

    @staticmethod
    def save_program(app):

        program = Saver.save_program_to_dict(app)
        fname = QFileDialog.getSaveFileName(app, 'Choose file', './program.pmp')[0]
        try:
            with open(fname, mode='w') as fout:
                json.dump(program, fout, sort_keys=True, indent=4)
        except:
            pass

    @staticmethod
    def save_program_to_dict(app):
        tape_elements = app.tape.tape_elements

        tape_data = dict(carriage=app.tape.get_carriage_index(), marked_cells=list())
        for index in tape_elements:
            if tape_elements[index].cell.is_marked:
                tape_data['marked_cells'].append(index)

        table_data = dict()
        count_rows = app.table_program.table.rowCount()
        for i in range(count_rows):
            command, comment, jump_state = '', '', ''
            try:
                command = app.table_program.table.item(i, 0).text()
                jump_state = app.table_program.table.item(i, 1).text()
                comment = app.table_program.table.item(i, 2).text()
            except AttributeError:
                pass
            table_data[i] = [command, jump_state, comment]

        program = {
            'tape': tape_data,
            'program': table_data,
        }

        return program
