# import json
#
# from tape import Tape
#
#
# class Loader:
#     @staticmethod
#     def load_program(app):
#         with open('test.json', mode='r') as fin:
#             program = json.load(fin)
#             tape_data = program['tape']
#             app.tape = Tape()
#             for cell in tape_data:
#
#             program_data = program['program']
