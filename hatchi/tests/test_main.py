"""Testing the main script"""
from hatchi.__main__ import main


def test_main() -> None:
    """Testing `main` function"""
    assert main(2, 3) == 5
