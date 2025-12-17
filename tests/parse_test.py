from pathlib import Path

from src.parse import parse_csv_file


class TestParseCsvFile:
    """Unit tests for parse_csv_file function."""

    def test_valid_csv_single_row(self, tmp_path: Path):
        """Test parsing a single valid row."""

        csv_content = """"name,position,completed_tasks,performance,skills,team,experience_years"
            John Doe,Developer,10,8.5,"Python,Testing",Alpha,5"""

        filepath = tmp_path / "test.csv"
        filepath.write_text(csv_content)
        result = parse_csv_file(filepath)

        assert len(result) == 1
        emp = result[0]
        assert emp.name == "John Doe"
        assert emp.position == "Developer"
        assert emp.completed_tasks == 10
        assert emp.performance == 8.5
        assert emp.skills == ["Python", "Testing"]
        assert emp.team == "Alpha"
        assert emp.experience_years == 5

    def test_multiple_valid_rows(self, tmp_path: Path):
        """Test parsing multiple valid rows."""

        csv_content = """name,position,completed_tasks,performance,skills,team,experience_years"
            Alice,Manager,5,9.2,"Leadership,PM",Beta,10
            Bob,Developer,15,7.8,"Python,Docker",Alpha,3"""

        filepath = tmp_path / "test.csv"
        filepath.write_text(csv_content)
        result = parse_csv_file(filepath)

        assert len(result) == 2
        assert result[0].name == "Alice"
        assert result[1].name == "Bob"

    def test_invalid_row_length(self, tmp_path: Path):
        """Test skipping rows with wrong number of columns."""

        csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
            Valid,Developer,10,8.5,"Python",Alpha,5
            Invalid,Dev,10,8.5,Alpha,5"""  # Only 6 columns

        filepath = tmp_path / "test.csv"
        filepath.write_text(csv_content)
        result = parse_csv_file(filepath)

        assert len(result) == 1
        assert result[0].position == "Developer"

    def test_invalid_numeric_values(self, tmp_path: Path):
        """Test skipping rows with invalid numeric data."""

        csv_content = """name,position,completed_tasks,performance,skills,team,experience_years"
            InvalidNum,Dev,abc,8.5,"Python",Alpha,xyz"""

        filepath = tmp_path / "test.csv"
        filepath.write_text(csv_content)
        result = parse_csv_file(filepath)

        assert len(result) == 0

    def test_empty_skills_list(self, tmp_path: Path):
        """Test empty skills string."""

        csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
            NoSkills,Dev,10,8.0,"",Alpha,2"""

        filepath = tmp_path / "test.csv"
        filepath.write_text(csv_content)
        result = parse_csv_file(filepath)

        assert result[0].skills == [""]

    def test_skills_with_spaces(self, tmp_path: Path):
        """Test skills parsing with extra spaces."""

        csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
            Spaced,Dev,10,8.0," Python , Docker ,  AWS",Alpha,2"""

        filepath = tmp_path / "test.csv"
        filepath.write_text(csv_content)
        result = parse_csv_file(filepath)

        assert result[0].skills == ["Python", "Docker", "AWS"]

    def test_empty_file(self, tmp_path: Path):
        """Test empty CSV file."""

        csv_content = (
            "name,position,completed_tasks,performance,skills,team,experience_years"
        )

        filepath = tmp_path / "test.csv"
        filepath.write_text(csv_content)
        result = parse_csv_file(filepath)

        assert len(result) == 0

    def test_file_not_found(self, tmp_path: Path):
        """Test file not found error."""

        filepath = tmp_path / "nonexistent.csv"
        result = parse_csv_file(str(filepath))

        assert len(result) == 0
