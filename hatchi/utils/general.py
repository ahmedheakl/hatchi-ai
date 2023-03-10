"""Utilties for training and testing models"""
import os


def get_device() -> str:
    """Retrieve the device name from the environment"""
    return os.environ["DEVICE"]
