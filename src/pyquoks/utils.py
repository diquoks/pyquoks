from __future__ import annotations
import datetime, sys, os


def get_path(relative_path: str, use_meipass: bool = False) -> str:
    """
    :param relative_path: Relative path of the file
    :param use_meipass: Whether or not ``sys._MEIPASS`` should be used
    :return: Absolute path for provided relative path
    """

    if use_meipass and hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_timestamp(date: datetime.datetime) -> int:
    return int(date.timestamp())
