"""Main script for Hatchi library"""
import logging

from utils.general import init_logger

_LOG = logging.getLogger(__name__)


def main(x_coord: int, y_coord: int) -> int:
    """Main function for the libray.
    Should be run as follows:
    """
    return x_coord + y_coord


if __name__ == "__main__":
    init_logger()
    _LOG.info(main(2, 3))
