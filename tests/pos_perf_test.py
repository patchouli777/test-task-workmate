from src.model import Employee
from src.pos_perf import PositionPerformance, handler_position_performance


class TestHandlerPositionPerformance:
    """Test suite for handler_position_performance function."""

    def test_single_employee(self):
        """Test with a single employee."""
        employee = Employee(
            name="John Doe",
            position="Developer",
            completed_tasks=10,
            performance=4.5,
            skills=["Python", "Testing"],
            team="Alpha",
            experience_years=5,
        )
        result = handler_position_performance([employee])

        expected: list[PositionPerformance] = [
            {"position": "Developer", "performance": 4.5}
        ]
        assert result == expected
        assert len(result) == 1
        assert result[0]["performance"] == 4.5

    def test_multiple_employees_same_position(self):
        """Test multiple employees in the same position."""
        employees = [
            Employee("Alice", "Developer", 12, 5.0, ["Python"], "Alpha", 3),
            Employee("Bob", "Developer", 8, 4.5, ["Java"], "Alpha", 4),
            Employee("Charlie", "Developer", 15, 4.8, ["Python"], "Beta", 6),
        ]
        result = handler_position_performance(employees)

        expected_performance = (
            employees[0].performance
            + employees[1].performance
            + employees[2].performance
        ) / 3
        expected: list[PositionPerformance] = [
            {"position": "Developer", "performance": expected_performance}
        ]
        assert len(result) == 1
        assert abs(result[0]["performance"] - expected[0]["performance"]) < 0.0001

    def test_multiple_positions(self):
        """Test employees across different positions."""
        employees = [
            Employee("Alice", "Developer", 12, 4.9, ["Python"], "Alpha", 3),
            Employee("Charlie", "Developer", 15, 4.8, ["Python"], "Beta", 6),
            Employee("Bob", "Manager", 5, 4.2, ["Leadership"], "Alpha", 10),
            Employee("Diana", "Manager", 8, 4.7, ["Leadership"], "Beta", 12),
        ]
        result = handler_position_performance(employees)

        exptected_dev_performance = (
            employees[0].performance + employees[1].performance
        ) / 2
        exptected_manager_performance = (
            employees[2].performance + employees[3].performance
        ) / 2
        expected: list[PositionPerformance] = [
            {"position": "Developer", "performance": exptected_dev_performance},
            {"position": "Manager", "performance": exptected_manager_performance},
        ]
        assert len(result) == 2
        assert result[0]["position"] == "Developer"
        assert result[1]["position"] == "Manager"
        assert abs(result[0]["performance"] - expected[0]["performance"]) < 0.0001
        assert abs(result[1]["performance"] - expected[1]["performance"]) < 0.0001

    def test_empty_list(self):
        """Test with empty employee list."""
        result = handler_position_performance([])
        assert result == []
        assert len(result) == 0

    def test_sorting_descending(self):
        """Test that results are sorted by performance descending."""
        employees = [
            Employee("Dev1", "Dev", 1, 4.5, [], "A", 1),
            Employee("Dev2", "Dev", 1, 5.0, [], "A", 1),
            Employee("Mgr1", "Mgr", 1, 4.5, [], "B", 1),
        ]
        result = handler_position_performance(employees)

        assert len(result) == 2
        assert result[0]["performance"] > result[1]["performance"]
        assert result[0]["position"] == "Dev"
        assert result[1]["position"] == "Mgr"

    def test_ties_in_performance(self):
        """Test handling of positions with identical average performance."""
        employees = [
            Employee("Dev1", "Developer", 1, 4.0, [], "A", 1),
            Employee("Dev2", "Developer", 1, 4.0, [], "A", 1),
            Employee("Mgr1", "Manager", 1, 4.0, [], "B", 1),
        ]
        result = handler_position_performance(employees)

        assert len(result) == 2
        assert result[0]["performance"] == 4.0
        assert result[1]["performance"] == 4.0

    def test_zero_performance(self):
        """Test employees with zero performance."""
        employees = [
            Employee("ZeroPerf", "Tester", 10, 0.0, ["Testing"], "Gamma", 2),
            Employee("GoodPerf", "Tester", 5, 4.5, ["Testing"], "Gamma", 3),
        ]
        result = handler_position_performance(employees)

        expected_avg = (employees[0].performance + employees[1].performance) / 2
        assert len(result) == 1
        assert abs(result[0]["performance"] - expected_avg) < 0.0001
