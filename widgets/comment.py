from PyQt5.QtWidgets import QPlainTextEdit


class Comment(QPlainTextEdit):

    def __init__(self, parent: any = None) -> None:
        super().__init__(parent=parent)
        pass
