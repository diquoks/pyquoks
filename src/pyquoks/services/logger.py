import datetime
import logging
import os
import sys
import typing

from .. import utils


class LoggerService(logging.Logger):
    """
    Class that provides methods for parallel logging

    Attributes:
        _LOG_PATH: Path to the logs file
    """

    _LOG_PATH: str | None

    def __init__(
            self,
            filename: str,
            level: int = logging.NOTSET,
            file_handling: bool = True,
            path: str = utils.get_path("logs/"),
    ) -> None:
        super().__init__(filename, level)

        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.stream_handler.setFormatter(
            logging.Formatter(
                fmt="$levelname $asctime $name - $message",
                datefmt="%d-%m-%y %H:%M:%S",
                style="$",
            )
        )
        self.addHandler(self.stream_handler)

        if file_handling:
            os.makedirs(
                name=path,
                exist_ok=True
            )
            self._LOG_PATH = path + f"{int(datetime.datetime.now().timestamp())}.{filename}.log"

            self.file_handler = logging.FileHandler(
                filename=self._LOG_PATH,
                encoding="utf-8",
            )
            self.file_handler.setFormatter(
                logging.Formatter(
                    fmt="$levelname $asctime - $message",
                    datefmt="%d-%m-%y %H:%M:%S",
                    style="$",
                ),
            )
            self.addHandler(self.file_handler)
        else:
            self._LOG_PATH = None

    @property
    def file(self) -> typing.IO | None:
        """
        :return: Opened file-like object of current logs
        """

        if self._LOG_PATH:
            return open(self._LOG_PATH, "rb")
        else:
            return None

    def log_exception(self, exception: Exception, raise_again: bool = False) -> None:
        """
        Logs an exception with detailed traceback

        :param exception: Exception to be logged
        :param raise_again: Whether or not exception should be raised again
        """

        self.error(
            msg=exception,
            exc_info=True,
        )

        if raise_again:
            raise exception
