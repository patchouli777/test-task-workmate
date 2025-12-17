from typing import TypedDict

from .model import Employee, Stat


class PositionPerformance(TypedDict):
    position: str
    performance: float


def handler_position_performance(employees: list[Employee]):
    """
    Calculates average performance for every position in employees array

    Args:
        employees: Array of employee objects

    Returns:
        Sorted list of average performance of employees grouped by position
    """
    position_to_stat: dict[str, Stat] = {}

    for emp in employees:
        if emp.position not in position_to_stat:
            position_to_stat[emp.position] = Stat(performance_sum=0, count=0)

        position_to_stat[emp.position].count += 1
        position_to_stat[emp.position].performance_sum += emp.performance

    result: list[PositionPerformance] = []
    for position, stat in position_to_stat.items():
        result.append({
            "position": position,
            "performance": stat.performance_sum / stat.count,
        })

    return sorted(result, key=lambda stat: stat["performance"], reverse=True)
