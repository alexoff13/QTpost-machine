import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCalendarWidget, QMainWindow, QGridLayout, QLayout, QTableWidget, QHeaderView, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox
from PyQt5.QtCore import QDate, Qt
from datetime import date, datetime


class CalendarWindow(QMainWindow):
    def __init__(self, parent=None):
        super(CalendarWindow, self).__init__(parent)
        self.setUpUI()

    def setUpUI(self):
        self.setGeometry(50, 50, 1200, 700)
        # Labels
        self.label_events = QLabel(self)
        self.label_new_event = QLabel(self)
        self.label_event_name = QLabel(self)
        self.label_start_date = QLabel(self)
        self.label_repeat = QLabel(self)
        self.label_description = QLabel(self)
        # Labels parameters
        self.label_events.setAlignment(Qt.AlignCenter)
        self.label_events.setText("Wydarzenia danego dnia:")

        self.label_new_event.setAlignment(Qt.AlignCenter)         # +
        self.label_new_event.setText("Dodaj event:")

        self.label_event_name.setText("Nazwa eventu:")
        self.label_start_date.setText("Data eventu:")
        self.label_repeat.setText("Powtarzalność eventu:")
        self.label_description.setText("Opis:")
        # TextEdits
        self.text_event_name = QLineEdit(self)
        self.text_start_date = QLineEdit(self)
        self.text_description = QLineEdit(self)
        # TextEdits parameters

        # ComboBoxes
        self.combo_repeat = QComboBox(self)
        # ComboBoxes parameters
        self.combo_repeat.addItems(
            ["No", "Day", "Week", "Two weeks", "Month", "Half a year", "Year"])

        # Widgets
        self.setWindowTitle("Python Calendar App")
        self.calendar_widget = QCalendarWidget(self)
        # User date select event
        self.calendar_widget.clicked[QDate].connect(self.dateChanged)
        self.events_list_widget = QTableWidget(self)
        self.events_list_widget.setColumnCount(5)
        self.events_list_widget.setHorizontalHeaderLabels(
            ["ID", "Name", "Date", "Repetition", "Description"])
        # Columns stretched and fit
        self.events_list_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.main_widget = QWidget(self)
        self.main_layout = QGridLayout(self.main_widget)
        self.main_layout.sizeConstraint = QLayout.SetDefaultConstraint
        self.main_layout.addWidget(self.calendar_widget, 0, 0)
        self.init_sublayouts()
        self.main_layout.addLayout(self.sublayout_events, 0, 1)
        self.main_layout.addLayout(self.sublayout_new_event, 0, 2)
        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 3)
        self.main_layout.setColumnStretch(2, 2)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def init_sublayouts(self):
        # Events sublayout
        self.sublayout_events = QVBoxLayout()
        self.sublayout_events.addWidget(self.label_events)
        self.sublayout_events.addWidget(self.events_list_widget)
        # New event sublayout
        self.sublayout_new_event = QVBoxLayout()
        self.sublayout_new_event.addWidget(self.label_new_event)
        self.sublayout_new_event.addStretch(1)                            # +

        self.sublayout_new_event_grid = QGridLayout()
        self.sublayout_new_event_grid.addWidget(self.label_event_name, 1, 0)
        self.sublayout_new_event_grid.addWidget(self.text_event_name, 1, 1)
        self.sublayout_new_event_grid.addWidget(self.label_start_date, 2, 0)
        self.sublayout_new_event_grid.addWidget(self.text_start_date, 2, 1)
        self.sublayout_new_event_grid.addWidget(self.label_repeat, 3, 0)
        self.sublayout_new_event_grid.addWidget(self.combo_repeat, 3, 1)
        self.sublayout_new_event_grid.addWidget(self.label_description, 4, 0)
        self.sublayout_new_event_grid.addWidget(self.text_description, 4, 1)
        self.sublayout_new_event.addLayout(self.sublayout_new_event_grid)
        self.sublayout_new_event.addStretch(20)                            # +

    def dateChanged(self, qdate):
        print("Date changed to:", self.getDaysEvents())
        selected_date = self.getDaysEvents()
        # self.events_list_widget.addItem(selected_date.strftime("%d/%m/%y"))

    def getDaysEvents(self):
        selected_date = self.calendar_widget.selectedDate()
        return selected_date.toPyDate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    foo = CalendarWindow()
    foo.show()
    sys.exit(app.exec_())
