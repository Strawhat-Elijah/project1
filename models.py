class Student:
    """Represents a single student with a name, scores, and final grade."""

    def __init__(self, name: str, scores: list) -> None:
        """
        Initialize a Student object.

        Args:
            name (str): The student's name.
            scores (list): List of attempt scores.
        """
        self.__name: str = name
        self.__scores: list = scores

    @property
    def name(self) -> str:
        """Return the student's name."""
        return self.__name

    @property
    def scores(self) -> list:
        """Return the student's scores."""
        return self.__scores

    def get_final_score(self) -> int:
        """Return the highest score from all attempts."""
        return max(self.__scores)

    def to_csv_row(self) -> list:
        """
        Return student data as a list for CSV writing.
        Pads to 4 attempts with 0s and appends the final score.
        """
        row = [self.__name]
        for score in self.__scores:
            row.append(score)
        while len(row) < 5:
            row.append(0)
        row.append(self.get_final_score())
        return row

    def __str__(self) -> str:
        """Return a readable string of the student."""
        return f"{self.__name} | Final: {self.get_final_score()}"