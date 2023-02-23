"""Collection for stats about code"""

PYLINT_FILE_NAME = "pylint.txt"
PYLINT_STATUS_NAME = "pylint_status.txt"
MYPY_FILE_NAME = "mypy.txt"
MYPY_STATUS_NAME = "mypy_status.txt"
LINTERS_FILE_NAME = "linters.txt"


def get_pylint_data() -> str:
    """Retrieve pylint data"""
    pylint_errors = ""
    with open(PYLINT_FILE_NAME, "r", encoding="utf-8") as pylint_file:
        for line in pylint_file.readlines():
            pylint_errors += line
    stat_data = ""
    with open(PYLINT_STATUS_NAME, "r", encoding="utf-8") as pylint_file:
        stat_data = pylint_file.readline()

    pylint_status: bool = int(stat_data) == 0
    if pylint_status:
        pylint_data = "* Pylint: ran :ok:"
    else:
        pylint_data = "<details><summary>Pylint: problems :warning: (click for details)</summary>\n"
        pylint_data += f"```python\n{pylint_errors}```\n"
        pylint_data += "</details>"
    return pylint_data


def main() -> None:
    """Main script for collecting stats"""
    linters_data = "#### Linters stats for Hatchi PR\n"
    linters_data += get_pylint_data()

    with open(LINTERS_FILE_NAME, "w", encoding="utf-8") as linters_file:
        linters_file.write(linters_data)


if __name__ == "__main__":
    main()
