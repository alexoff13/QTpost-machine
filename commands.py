from threading import Thread
from time import sleep

from main import App
from utils import Saver
from utils.loader import Loader


def func(a):
    pass


def set_a_label(to_state: str, app: App) -> int:
    app.tape.inverse_carriage()
    print('set_a_label', int(to_state))
    return int(to_state) - 1


def reset_a_label(to_state: str, app: App) -> int:
    app.tape.inverse_carriage(need_to_mark=False)
    return int(to_state) - 1


def go_to_right(to_state: str, app: App) -> int:
    app.tape.go_right()
    print('go_to right', int(to_state))
    return int(to_state) - 1


def go_to_left(to_state: str, app: App) -> int:
    app.tape.go_left()
    return int(to_state) - 1


def exit(to_state: str, app: App) -> int:
    return -1


commands = {
    '+': set_a_label,
    'x': reset_a_label,
    '>': go_to_right,
    '<': go_to_left,
    '?': func,
    '!': exit,
}


def run_program(app: App):
    th = Thread(target=run_program_, args=(app, ))
    th.start()
    # run_program_(app)


def run_program_(app: App):
    program = Saver.save_program_to_dict(app)
    i = 0
    while i != -1:
        sleep(0.5)
        print(i)
        try:
            i = commands[app.table_program.table.item(i, 0).text()](app.table_program.table.item(i, 1).text(), app)
        except:
            break
    # sleep(10)
    # Loader.load_program_from_dict(program, app)

