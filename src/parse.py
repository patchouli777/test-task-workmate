import csv
import itertools
from pathlib import Path

from .model import Employee


def parse_csv_files(filenames: list[str]) -> list[Employee]:
    """
    Parse CSV files into a list of Employee dataclasses.

    Args:
        filenames: Array of paths to CSV files

    Returns:
        List of Employee objects
    """
    data: list[list[Employee]] = []

    for filename in filenames:
        data.append(parse_csv_file(filename))

    return list(itertools.chain.from_iterable(data))


def parse_csv_file(filename: str | Path) -> list[Employee]:
    """
    Parse a CSV file into a list of Employee dataclasses.

    Args:
        filename: Path to the CSV file

    Returns:
        List of Employee objects
    """
    stats: list[Employee] = []
    path = Path(filename)

    try:
        with path.open("r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row_num, row in enumerate(reader, start=1):
                if len(row) != 7:
                    print(
                        f"Warning: Row {row_num} in {filename} has {len(row)} columns, expected 7. Skipping."
                    )
                    continue

                try:
                    (
                        name,
                        position,
                        completed_tasks_str,
                        performance_str,
                        skills_str,
                        team,
                        experience_str,
                    ) = row

                    completed_tasks = int(completed_tasks_str)
                    performance = float(performance_str)
                    experience_years = int(experience_str)

                    skills = [
                        skill.strip() for skill in skills_str.strip('"').split(",")
                    ]

                    stat = Employee(
                        name=name.strip(),
                        position=position.strip(),
                        completed_tasks=completed_tasks,
                        performance=performance,
                        skills=skills,
                        team=team.strip(),
                        experience_years=experience_years,
                    )
                    stats.append(stat)

                except (ValueError, IndexError) as e:
                    print(f"Warning: Error parsing row {row_num} in {filename}: {e}")
                    continue

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading '{filename}': {str(e)}")

    return stats
