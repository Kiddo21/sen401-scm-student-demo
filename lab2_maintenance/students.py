"""Maintained student records module for SEN 401 Lab 2.

Maintenance included empty-list handling, input validation, clearer output,
median calculation, type hints, and reusable functions.
"""

from statistics import mean, median
from typing import TypedDict


class Student(TypedDict):
    """Shape of one student record."""

    name: str
    score: float


students: list[Student] = [
    {"name": "James", "score": 45},
    {"name": "Deborah", "score": 82},
    {"name": "Amina", "score": 76},
    {"name": "Chinedu", "score": 91},
]


def validate_student(name: str, score: int | float) -> Student:
    """Validate and return a student record.

    Scores are limited to the inclusive range 0–100. Boolean values are
    rejected even though bool is a subclass of int in Python.
    """
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Student name must be a non-empty string.")
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise TypeError("Student score must be a number.")
    if not 0 <= score <= 100:
        raise ValueError("Student score must be between 0 and 100.")
    return {"name": name.strip(), "score": float(score)}


def validate_students(data: list[Student]) -> None:
    """Raise a clear exception if any student record is malformed."""
    for index, student in enumerate(data, start=1):
        if not isinstance(student, dict):
            raise TypeError(f"Record {index} must be a dictionary.")
        validate_student(student.get("name"), student.get("score"))


def average_score(data: list[Student] | None = None) -> float:
    """Return the arithmetic mean, or 0.0 when the list is empty."""
    records = students if data is None else data
    if not records:
        return 0.0
    validate_students(records)
    return round(mean(record["score"] for record in records), 2)


def median_score(data: list[Student] | None = None) -> float:
    """Return the median score, or 0.0 when the list is empty."""
    records = students if data is None else data
    if not records:
        return 0.0
    validate_students(records)
    return float(median(record["score"] for record in records))


def highest_score(data: list[Student] | None = None) -> Student | None:
    """Return the highest-scoring student, or None for an empty list."""
    records = students if data is None else data
    if not records:
        return None
    validate_students(records)
    return max(records, key=lambda record: record["score"])


def lowest_score(data: list[Student] | None = None) -> Student | None:
    """Return the lowest-scoring student, or None for an empty list."""
    records = students if data is None else data
    if not records:
        return None
    validate_students(records)
    return min(records, key=lambda record: record["score"])


def add_student(name: str, score: int | float) -> Student:
    """Validate a new record, append it to the shared list, and return it."""
    record = validate_student(name, score)
    students.append(record)
    return record


def print_report(data: list[Student] | None = None) -> None:
    """Print a formatted student list and statistics."""
    records = students if data is None else data
    print("\nSTUDENT RESULTS")
    print("-" * 48)
    if not records:
        print("No student records are available.")
        print("-" * 48)
        print("Average: 0.00 | Median: 0.00")
        return

    validate_students(records)
    for number, record in enumerate(records, start=1):
        print(f"{number:>2}. {record['name']:<20} {record['score']:>6.2f}%")

    top = highest_score(records)
    bottom = lowest_score(records)
    print("-" * 48)
    print(f"Average score : {average_score(records):.2f}%")
    print(f"Median score  : {median_score(records):.2f}%")
    assert top is not None and bottom is not None
    print(f"Highest score : {top['name']} ({top['score']:.2f}%)")
    print(f"Lowest score  : {bottom['name']} ({bottom['score']:.2f}%)")


if __name__ == "__main__":
    print_report()
