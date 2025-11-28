# gradebook.py
# this was generated for me by ChatGPT
from typing import Dict, Optional


class GradeBook:
    """
    GradeBook tracks numeric scores for students and can compute
    averages, letter grades, and class statistics.

    Design goals:
    - Easy to read and understand.
    - Enough behavior/branches to support many test cases.
    """

    def __init__(self, passing_score: float = 60.0) -> None:
        """
        Create a new GradeBook.

        :param passing_score: Minimum average score considered "passing".
                              Must be a number between 0 and 100 inclusive.
        :raises TypeError: if passing_score is not a number.
        :raises ValueError: if passing_score is outside [0, 100].
        """
        if not isinstance(passing_score, (int, float)):
            raise TypeError("passing_score must be a number")

        if passing_score < 0 or passing_score > 100:
            raise ValueError("passing_score must be between 0 and 100")

        self._passing_score: float = float(passing_score)
        # _students maps student_name -> { assignment_name -> score }
        self._students: Dict[str, Dict[str, float]] = {}
        self._locked: bool = False

    # ------------------------------------------------------------------
    # Basic state / properties
    # ------------------------------------------------------------------

    @property
    def passing_score(self) -> float:
        """Return the configured passing score."""
        return self._passing_score

    @property
    def is_locked(self) -> bool:
        """True if the gradebook is locked against modifications."""
        return self._locked

    def lock(self) -> None:
        """Prevent further modifications to students and scores."""
        self._locked = True

    def unlock(self) -> None:
        """Allow modifications again."""
        self._locked = False

    def __len__(self) -> int:
        """Return the number of students in the gradebook."""
        return len(self._students)

    # ------------------------------------------------------------------
    # Student management
    # ------------------------------------------------------------------

    def add_student(self, name: str) -> None:
        """
        Add a new student.

        :param name: Non-empty string name.
        :raises RuntimeError: if gradebook is locked.
        :raises ValueError: if name is empty or already exists.
        """
        if self._locked:
            raise RuntimeError("GradeBook is locked; cannot add students")

        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Student name must be a non-empty string")

        if name in self._students:
            raise ValueError(f"Student '{name}' already exists")

        self._students[name] = {}

    def remove_student(self, name: str) -> None:
        """
        Remove a student and all their scores.

        :raises RuntimeError: if gradebook is locked.
        :raises KeyError: if student does not exist.
        """
        if self._locked:
            raise RuntimeError("GradeBook is locked; cannot remove students")

        try:
            del self._students[name]
        except KeyError:
            raise KeyError(f"Student '{name}' not found") from None

    def has_student(self, name: str) -> bool:
        """Return True if the student exists in the gradebook."""
        return name in self._students

    # ------------------------------------------------------------------
    # Scores
    # ------------------------------------------------------------------

    def _require_student(self, name: str) -> Dict[str, float]:
        if name not in self._students:
            raise KeyError(f"Student '{name}' not found")
        return self._students[name]

    @staticmethod
    def _validate_score(score: float) -> float:
        """
        Ensure score is a number between 0 and 100 inclusive.

        :raises TypeError: if not a number.
        :raises ValueError: if outside [0, 100].
        """
        if not isinstance(score, (int, float)):
            raise TypeError("Score must be numeric")
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100")
        return float(score)

    def set_score(self, student: str, assignment: str, score: float) -> None:
        """
        Set or overwrite a score for a specific assignment.

        :raises RuntimeError: if gradebook is locked.
        :raises KeyError: if student does not exist.
        :raises ValueError: if assignment name is empty.
        :raises TypeError/ValueError: for invalid score.
        """
        if self._locked:
            raise RuntimeError("GradeBook is locked; cannot modify scores")

        if not isinstance(assignment, str) or assignment.strip() == "":
            raise ValueError("Assignment name must be a non-empty string")

        scores_for_student = self._require_student(student)
        scores_for_student[assignment] = self._validate_score(score)

    def get_score(
        self, student: str, assignment: str, default: Optional[float] = None
    ) -> Optional[float]:
        """
        Get the score for a specific assignment.

        :param default: Value to return if assignment has no score.
        :raises KeyError: if student does not exist.
        """
        scores_for_student = self._require_student(student)
        return scores_for_student.get(assignment, default)

    def clear_score(self, student: str, assignment: str) -> bool:
        """
        Remove a specific assignment score for a student.

        :return: True if a score was removed, False if none existed.
        :raises RuntimeError: if gradebook is locked.
        :raises KeyError: if student does not exist.
        """
        if self._locked:
            raise RuntimeError("GradeBook is locked; cannot modify scores")

        scores_for_student = self._require_student(student)
        if assignment in scores_for_student:
            del scores_for_student[assignment]
            return True
        return False

    # ------------------------------------------------------------------
    # Calculations
    # ------------------------------------------------------------------

    def student_average(self, student: str) -> Optional[float]:
        """
        Return the average score for a student, or None if they have no scores.

        :raises KeyError: if student does not exist.
        """
        scores_for_student = self._require_student(student)
        if not scores_for_student:
            return None
        total = sum(scores_for_student.values())
        return total / len(scores_for_student)

    def class_average(self) -> Optional[float]:
        """
        Return the average of all student averages.

        Students with no scores are ignored.
        Returns None if no student has any scores.
        """
        averages = []
        for name in self._students:
            avg = self.student_average(name)
            if avg is not None:
                averages.append(avg)

        if not averages:
            return None

        return sum(averages) / len(averages)

    def letter_grade(self, student: str) -> Optional[str]:
        """
        Return the letter grade (A/B/C/D/F) for a student based on their average.

        Returns None if the student has no scores.

        Scale:
            90-100: A
            80-89:  B
            70-79:  C
            60-69:  D
            <60:    F
        """
        avg = self.student_average(student)
        if avg is None:
            return None

        if avg >= 90:
            return "A"
        if avg >= 80:
            return "B"
        if avg >= 70:
            return "C"
        if avg >= 60:
            return "D"
        return "F"

    def has_passing_grade(self, student: str) -> Optional[bool]:
        """
        Return True if the student's average is >= passing_score,
        False if below passing_score, or None if they have no scores.
        """
        avg = self.student_average(student)
        if avg is None:
            return None
        return avg >= self._passing_score

    def drop_lowest_score(self, student: str) -> bool:
        """
        Drop the lowest assignment score for a student.

        :return: True if a score was dropped, False if the student had
                 zero or one score.
        :raises RuntimeError: if gradebook is locked.
        :raises KeyError: if student does not exist.
        """
        if self._locked:
            raise RuntimeError("GradeBook is locked; cannot modify scores")

        scores_for_student = self._require_student(student)
        if len(scores_for_student) <= 1:
            return False

        # Find the assignment with the lowest score
        lowest_assignment = min(
            scores_for_student, key=lambda a: scores_for_student[a]
        )
        del scores_for_student[lowest_assignment]
        return True

    def curve_student(self, student: str, points: float) -> None:
        """
        Add a fixed number of points to all of a student's scores.

        Scores are clamped to [0, 100].

        :raises RuntimeError: if gradebook is locked.
        :raises KeyError: if student does not exist.
        :raises TypeError: if points is not numeric.
        """
        if self._locked:
            raise RuntimeError("GradeBook is locked; cannot modify scores")

        if not isinstance(points, (int, float)):
            raise TypeError("points must be numeric")

        scores_for_student = self._require_student(student)
        for assignment, score in list(scores_for_student.items()):
            new_score = score + points
            if new_score < 0:
                new_score = 0.0
            elif new_score > 100:
                new_score = 100.0
            scores_for_student[assignment] = new_score

    def top_student(self) -> Optional[str]:
        """
        Return the name of the student with the highest average.

        Students with no scores are ignored.
        Returns None if no student has any scores.
        """
        best_name = None
        best_avg = None

        for name in self._students:
            avg = self.student_average(name)
            if avg is None:
                continue
            if best_avg is None or avg > best_avg:
                best_avg = avg
                best_name = name

        return best_name

