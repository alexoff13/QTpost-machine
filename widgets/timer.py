from PyQt5.QtWidgets import QDoubleSpinBox, QLineEdit


class Timer(QDoubleSpinBox):
    MIN = 0
    MAX = 5
    DECIMALS = 2
    STEP = 0.01
    UNIT = ' sec'
    SPECIAL_VALUE = 'max'

    def __init__(self, parent: any = None) -> None:
        super().__init__(parent=parent)
        self.setRange(self.MIN, self.MAX)
        self.setDecimals(self.DECIMALS)
        self.setSingleStep(self.STEP)
        self.setSuffix(self.UNIT)
        self.setFixedSize(80, 20)
        self.setSpecialValueText(self.SPECIAL_VALUE)
        self.setLineEdit(QLineEdit())
