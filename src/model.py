from dataclasses import dataclass


@dataclass
class Employee:
    name: str
    position: str
    completed_tasks: int
    performance: float
    skills: list[str]
    team: str
    experience_years: int


@dataclass
class Stat:
    performance_sum: float
    count: int
