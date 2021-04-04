import json


class Saver:
    @staticmethod
    def save_program(app):
        cells = app.tape.cells
        states_cells = list()
        for index in cells.keys():
            states_cells.append([index, cells[index].is_marked])

        table_data = dict()
        count_rows = app.tableWidget.rowCount()
        for i in range(count_rows):
            command, comment, jump_state = '', '', ''
            try:
                command = app.tableWidget.item(i, 0).text()
                jump_state = app.tableWidget.item(i, 1).text()
                comment = app.tableWidget.item(i, 2).text()
            except AttributeError:
                pass
            table_data[i] = [command, jump_state, comment]

        program = {
            'tape': states_cells,
            'program': table_data,
        }

        with open('test.json', mode='w') as fout:
            fout.writelines(json.dumps(program, sort_keys=True, indent=4))
