from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QLineEdit,
    QWidget, QHBoxLayout, QVBoxLayout, QLabel
)


class Ui_MainWindow(object):
    """Generated UI class from QT Designer."""

    def setupUi(self, MainWindow: QMainWindow) -> None:
        """Set up the UI components on the main window."""
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 500)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.name_input = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.name_input.setMaximumSize(QtCore.QSize(200, 16777215))
        self.name_input.setObjectName("name_input")
        self.horizontalLayout.addWidget(self.name_input)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.attempts_input = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.attempts_input.setMaximumSize(QtCore.QSize(200, 16777215))
        self.attempts_input.setObjectName("attempts_input")
        self.horizontalLayout_2.addWidget(self.attempts_input)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.generate_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.generate_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.generate_button.setObjectName("generate_button")
        self.horizontalLayout_3.addWidget(self.generate_button)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.submit_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.submit_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.submit_button.setObjectName("submit_button")
        self.horizontalLayout_4.addWidget(self.submit_button)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.status_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.status_label.setObjectName("status_label")
        self.horizontalLayout_5.addWidget(self.status_label)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.save_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.save_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.save_button.setObjectName("save_button")
        self.horizontalLayout_6.addWidget(self.save_button)
        self.verticalLayout.addLayout(self.horizontalLayout_6)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow: QMainWindow) -> None:
        """Set the text for all UI components."""
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Student Grade Manager"))
        self.label.setText(_translate("MainWindow", "Student name:"))
        self.label_2.setText(_translate("MainWindow", "No of attempts:"))
        self.generate_button.setText(_translate("MainWindow", "Generate Score Fields"))
        self.submit_button.setText(_translate("MainWindow", "SUBMIT"))
        self.status_label.setText(_translate("MainWindow", ""))
        self.save_button.setText(_translate("MainWindow", "Save to CSV"))


class GradeAppWindow(QMainWindow, Ui_MainWindow):
    """Main application window combining QMainWindow and generated UI."""

    def __init__(self) -> None:
        """Initialize the window and set up the UI."""
        super().__init__()
        self.setupUi(self)
        self.__score_inputs: list = []
        self.__scores_container = QVBoxLayout()
        self.verticalLayout.insertLayout(3, self.__scores_container)
        self.submit_button.setVisible(False)
        self.save_button.setVisible(False)
        self.status_label.setText("")
        self.generate_button.clicked.connect(self.__generate_score_fields)

    def __generate_score_fields(self) -> None:
        """Dynamically generate score input fields based on number of attempts."""
        attempts_text = self.attempts_input.text().strip()

        try:
            attempts = int(attempts_text)
        except ValueError:
            QMessageBox.critical(self, "Error", "Attempts must be a number.")
            return

        if attempts < 1 or attempts > 4:
            QMessageBox.critical(self, "Error", "Attempts must be between 1 and 4.")
            return

        self.__score_inputs = []
        while self.__scores_container.count():
            item = self.__scores_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for i in range(attempts):
            row_widget = QWidget()
            row = QHBoxLayout(row_widget)
            row.addWidget(QLabel(f"Score {i + 1}:"))
            score_field = QLineEdit()
            score_field.setMaximumWidth(200)
            row.addWidget(score_field)
            self.__score_inputs.append(score_field)
            self.__scores_container.addWidget(row_widget)

        self.submit_button.setVisible(True)

    def get_name(self) -> str:
        """Return the student name input text."""
        return self.name_input.text().strip()

    def get_scores(self) -> list:
        """Return list of score strings from dynamic score fields."""
        return [field.text().strip() for field in self.__score_inputs]

    def show_status(self, message: str, color: str = "red") -> None:
        """Display a status message in the given color."""
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color};")

    def show_save_button(self) -> None:
        """Make the Save to CSV button visible."""
        self.save_button.setVisible(True)

    def clear_inputs(self) -> None:
        """Clear all input fields and hide the submit button."""
        self.name_input.clear()
        self.attempts_input.clear()
        self.__score_inputs = []
        while self.__scores_container.count():
            item = self.__scores_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.submit_button.setVisible(False)

    def connect_submit(self, handler) -> None:
        """Connect the submit button to a handler function."""
        self.submit_button.clicked.connect(handler)

    def connect_save(self, handler) -> None:
        """Connect the save button to a handler function."""
        self.save_button.clicked.connect(handler)

    def show_error(self, message: str) -> None:
        """Show an error dialog."""
        QMessageBox.critical(self, "Error", message)