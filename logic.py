import csv
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from models import Student


class GradeCalculator:
    """Handles grade calculation and CSV file operations."""

    def __init__(self) -> None:
        """Initialize with an empty student list."""
        self.__students: list = []

    def add_student(self, name: str, scores: list) -> None:
        """Create and add a new Student to the list."""
        student = Student(name, scores)
        self.__students.append(student)

    def get_best_score(self) -> int:
        """Return the highest final score among all students."""
        if not self.__students:
            return 0
        return max(student.get_final_score() for student in self.__students)

    def assign_grade(self, final_score: int) -> str:
        """Return the letter grade for a given score using the Lab 2 scheme."""
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

    def clear_students(self) -> None:
        """Clear all students from the list."""
        self.__students = []

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
        """
        Save all student data to a CSV file with a computational summary row.

        Args:
            file_path (str): Path to the output CSV file.

        Raises:
            IOError: If the file cannot be written.
        """
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


class GradeManagerController:
    """Connects the GUI window to the GradeCalculator logic."""

    def __init__(self) -> None:
        """Initialize the controller with a calculator and window."""
        from gui import GradeAppWindow
        self.__calculator = GradeCalculator()
        self.__window = GradeAppWindow()
        self.__window.connect_submit(self.__handle_submit)
        self.__window.connect_save(self.__handle_save)

    def show(self) -> None:
        """Display the main application window."""
        self.__window.show()

    def __handle_submit(self) -> None:
        """Validate input and submit a student record."""
        name = self.__window.get_name()
        scores_text = self.__window.get_scores()

        if not name:
            self.__window.show_error("Student name cannot be empty.")
            return

        scores = []
        for i, score_text in enumerate(scores_text):
            try:
                score = int(score_text)
            except ValueError:
                self.__window.show_error(
                    f"Score {i + 1} must be a whole number.")
                return
            if score < 0 or score > 100:
                self.__window.show_error(
                    f"Score {i + 1} must be between 0 and 100.")
                return
            scores.append(score)

        self.__calculator.add_student(name, scores)
        self.__window.show_status("Submitted", color="red")
        self.__window.show_save_button()
        self.__window.clear_inputs()

    def __handle_save(self) -> None:
        """Open a file dialog and save student data to CSV."""
        if not self.__calculator.get_students():
            self.__window.show_error("No students to save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self.__window, "Save Grades", "", "CSV Files (*.csv)"
        )
        if not file_path:
            return
        try:
            self.__calculator.save_to_csv(file_path)
            QMessageBox.information(self.__window, "Saved",
                                    f"Grades saved to:\n{file_path}")
        except IOError as e:
            self.__window.show_error(str(e))