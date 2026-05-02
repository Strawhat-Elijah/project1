import csv
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from gui import *
from models import Student


class GradeCalculator:
    """Handles grade calculation and CSV file operations."""

    def __init__(self) -> None:
        """Initialize with an empty student list."""
        self.__students: list = []

    def add_student(self, name: str, scores: list) -> None:
        """
        Add a new student to the list.

        Args:
            name (str): Student name.
            scores (list): List of attempt scores.
        """
        student = Student(name, scores)
        self.__students.append(student)

    def get_best_score(self) -> int:
        """Return the highest final score among all students."""
        if not self.__students:
            return 0
        return max(student.get_final_score() for student in self.__students)

    def assign_grade(self, final_score: int) -> str:
        """
        Return the letter grade for a given score.

        Args:
            final_score (int): The student's highest score.

        Returns:
            str: Letter grade A, B, C, D, or F.
        """
        best = self.get_best_score()
        if final_score >= best - 10:
            return "A"
        elif final_score >= best - 20:
            return "B"
        elif final_score >= best - 30:
            return "C"
        elif final_score >= best - 40:
            return "D"
        else:
            return "F"

    def get_students(self) -> list:
        """Return a copy of the student list."""
        return list(self.__students)

    def get_highest_final(self) -> int:
        """Return the highest final score across all students."""
        if not self.__students:
            return 0
        return max(student.get_final_score() for student in self.__students)

    def get_lowest_final(self) -> int:
        """Return the lowest final score across all students."""
        if not self.__students:
            return 0
        return min(student.get_final_score() for student in self.__students)

    def get_average_final(self) -> float:
        """Return the average final score across all students."""
        if not self.__students:
            return 0.0
        total = sum(student.get_final_score() for student in self.__students)
        return round(total / len(self.__students), 2)

    def save_to_csv(self, file_path: str) -> None:
        try:
            with open(file_path, "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Name", "Score 1", "Score 2",
                                 "Score 3", "Score 4", "Final"])
                for student in self.__students:
                    writer.writerow(student.to_csv_row())
                writer.writerow([])
                writer.writerow(["Highest", "", "", "", "",
                                 self.get_highest_final()])
                writer.writerow(["Lowest", "", "", "", "",
                                 self.get_lowest_final()])
                writer.writerow(["Average", "", "", "", "",
                                 self.get_average_final()])
        except IOError as e:
            raise IOError(f"Could not save file: {e}")


# AI assisted with PyQt6 window structure
class Logic(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        """Initialize the window, set up UI, and connect buttons."""
        super().__init__()
        self.setupUi(self)
        self.__calculator = GradeCalculator()
        self.__score_inputs: list = []
        self.__scores_container = QVBoxLayout()
        self.verticalLayout.insertLayout(3, self.__scores_container)
        self.submit_button.setVisible(False)
        self.save_button.setVisible(False)
        self.status_label.setText("")
        self.generate_button.clicked.connect(self.__generate_score_fields)
        self.submit_button.clicked.connect(self.__handle_submit)
        self.save_button.clicked.connect(self.__handle_save)

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

    def __handle_submit(self) -> None:
        """Validate input and submit a student record."""
        name = self.name_input.text().strip()
        scores_text = [field.text().strip() for field in self.__score_inputs]

        if not name:
            QMessageBox.critical(self, "Error", "Student name cannot be empty.")
            return

        scores = []
        for i, score_text in enumerate(scores_text):
            try:
                score = int(score_text)
            except ValueError:
                QMessageBox.critical(self, "Error",
                                     f"Score {i + 1} must be a whole number.")
                return
            if score < 0 or score > 100:
                QMessageBox.critical(self, "Error",
                                     f"Score {i + 1} must be between 0 and 100.")
                return
            scores.append(score)

        self.__calculator.add_student(name, scores)
        self.status_label.setText("Submitted")
        self.status_label.setStyleSheet("color: red;")
        self.save_button.setVisible(True)

        self.name_input.clear()
        self.attempts_input.clear()
        self.__score_inputs = []
        while self.__scores_container.count():
            item = self.__scores_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.submit_button.setVisible(False)

    def __handle_save(self) -> None:
        """Open a file dialog and save student data to CSV."""
        if not self.__calculator.get_students():
            QMessageBox.critical(self, "Error", "No students to save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Grades", "", "CSV Files (*.csv)"
        )
        if not file_path:
            return
        try:
            self.__calculator.save_to_csv(file_path)
            QMessageBox.information(self, "Saved",
                                    f"Grades saved to:\n{file_path}")
        except IOError as e:
            QMessageBox.critical(self, "Error", str(e))