from PyQt5.QtWidgets import QPlainTextEdit


class Comment(QPlainTextEdit):

    def __init__(self, parent: any = None) -> None:
        super().__init__(parent=parent)

    def get_data(self) -> str:
        return self.toPlainText()

    def set_from_file(self, file: str) -> None:
        self.setPlainText(file)
