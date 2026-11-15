"""Reusable helper functions for working with student scores."""

from statistics import mean
from typing import Any

Student = dict[str, Any]


def _validated_students(data: list[Student]) -> list[Student]:
    """Return records with a non-empty name and a numeric score."""
    valid: list[Student] = []
    for position, student in enumerate(data, start=1):
        if not isinstance(student, dict):
            raise TypeError(f"Student record {position} must be a dictionary.")
        name = student.get("name")
        score = student.get("score")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Student record {position} has an invalid name.")
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise ValueError(f"Student record {position} has an invalid score.")
        if not 0 <= score <= 100:
            raise ValueError(f"Score for {name} must be between 0 and 100.")
        valid.append(student)
    return valid


def average_score(data: list[Student]) -> float:
    """Calculate the average score; return 0.0 for an empty list."""
    valid = _validated_students(data)
    return round(mean(student["score"] for student in valid), 2) if valid else 0.0


def highest_score(data: list[Student]) -> Student | None:
    """Return the student with the highest score, or None if no records exist."""
    valid = _validated_students(data)
    return max(valid, key=lambda student: student["score"], default=None)


def lowest_score(data: list[Student]) -> Student | None:
    """Return the student with the lowest score, or None if no records exist."""
    valid = _validated_students(data)
    return min(valid, key=lambda student: student["score"], default=None)
