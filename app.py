"""Run a small student-performance demonstration."""

from students import students
from utils.helpers import average_score, highest_score, lowest_score


def main() -> None:
    """Display student records and a short performance summary."""
    print("=" * 52)
    print("             STUDENT PERFORMANCE REPORT")
    print("=" * 52)

    if not students:
        print("No student records are currently available.")
        return

    for number, student in enumerate(students, start=1):
        print(f"{number:>2}. {student['name']:<18} {student['score']:>5.1f}%")

    top_student = highest_score(students)
    low_student = lowest_score(students)
    print("-" * 52)
    print(f"Average score : {average_score(students):.2f}%")
    print(f"Highest score : {top_student['name']} ({top_student['score']}%)")
    print(f"Lowest score  : {low_student['name']} ({low_student['score']}%)")
    print("=" * 52)


if __name__ == "__main__":
    main()
