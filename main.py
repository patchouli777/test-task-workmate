import argparse
from typing import Any, Callable

import tabulate

from src.model import Employee
from src.parse import parse_csv_files
from src.pos_perf import handler_position_performance

type ProcessFuncReturn = list[dict[str, Any]] | str
type ProcessFunc = Callable[[list[Employee]], ProcessFuncReturn]


def process(employees: list[Employee], func: ProcessFunc):
    return func(employees)


def handler_default(employees: list[Employee]) -> str:
    return "Error: unknown report type. Available report types: performance, example1."


handlers: dict[str, Callable[[list[Employee]], list[Any] | str]] = {
    "performance": handler_position_performance,
    "example1": handler_position_performance,
}


def main():
    parser = argparse.ArgumentParser(description="Read files")
    parser.add_argument("--files", nargs="+", help="One or more filenames to read")
    parser.add_argument(
        "--report",
        nargs="?",
        help="Type of report. Available: performance, example1.",
    )

    args = parser.parse_args()
    employees = parse_csv_files(args.files)

    result = process(employees, handlers.get(args.report, handler_default))
    if isinstance(result, str):
        print(result)
    else:
        print(
            tabulate.tabulate(
                result, showindex="always", headers="keys", floatfmt=".2f"
            )
        )


if __name__ == "__main__":
    main()
