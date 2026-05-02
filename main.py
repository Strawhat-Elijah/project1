import sys
from PyQt6.QtWidgets import QApplication
from logic import GradeManagerController
 
 
def main() -> None:
    """Launch the Student Grade Manager application."""
    app = QApplication(sys.argv)
    controller = GradeManagerController()
    controller.show()
    sys.exit(app.exec())
 
 
if __name__ == "__main__":
    main()
 