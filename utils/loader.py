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
        return program


