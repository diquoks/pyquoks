from __future__ import annotations
import datetime, logging, typing, sys, os
import pyquoks.utils


# region Services

class LoggerService(logging.Logger):
    """
    Class that provides methods for parallel logging

    Attributes:
        _LOG_PATH: Path to the logs file
    """

    _LOG_PATH: str | None

    def __init__(
            self,
            name: str,
            level: int = logging.NOTSET,
            file_handling: bool = True,
            path: str = pyquoks.utils.get_path("logs/"),
            filename: str = str(int(datetime.datetime.now().timestamp())),
    ) -> None:
        super().__init__(name, level)

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
            os.makedirs(path, exist_ok=True)
            self._LOG_PATH = path + f"{filename}.{name}.log"

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

    @property
    def file(self) -> typing.BinaryIO | None:
        """
        :return: Opened file-like object of current logs
        """

        if self._LOG_PATH:
            return open(self._LOG_PATH, "rb")
        else:
            return None

    def log_error(self, exception: Exception) -> None:
        """
        Logs an exception with detailed traceback
        """

        self.error(
            msg=exception,
            exc_info=True,
        )

# endregion
