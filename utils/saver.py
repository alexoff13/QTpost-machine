import json

from PyQt5.QtWidgets import QFileDialog


class Saver:
    @staticmethod
    def save_program(app):
        cells = app.tape.cells
        states_cells = list()
        for index in cells.keys():
            states_cells.append([index, cells[index].is_marked])

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
            'tape': states_cells,
            'program': table_data,
        }
        fname = QFileDialog.getSaveFileName(app, 'Choose file', './program.pmp')[0]
        try:
            with open(fname, mode='w') as fout:
                json.dump(program, fout, sort_keys=True, indent=4)
        except:
            pass
