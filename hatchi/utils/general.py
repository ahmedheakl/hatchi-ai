"""Utilties for training and testing models"""
from typing import Union
import os
import logging
import coloredlogs


def get_device() -> str:
    """Retrieve the device name from the environment"""
    return os.environ["DEVICE"]


def init_logger(level: Union[int, str] = logging.INFO) -> None:
    """Initialize logger with desired configs

    Args:
        debug (bool, optional): Whether to output debug info to the console. Defaults to False.

    Returns:
        logging.Logger: Logger instance with desired configs
    """
    to_log_level = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    if isinstance(level, str):
        assert level in to_log_level, "Invalid level name"
        log_level = to_log_level[level]
    else:
        log_level = level

    logs_dir = os.path.join(os.path.expanduser("~"), ".logs")

    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)

    filename = "hatchi.log"
    logs_path = os.path.join(logs_dir, filename)

    # initialize file handler
    f_handler = logging.FileHandler(filename=logs_path, mode="w")
    f_handler.setLevel(logging.DEBUG)
    f_format = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )
    f_handler.setFormatter(f_format)

    # set handlers
    logging.basicConfig(handlers=[f_handler])

    # initialize colored logs
    coloredlogs.install(
        fmt="%(asctime)s - %(message)s",
        level=log_level,
    )
