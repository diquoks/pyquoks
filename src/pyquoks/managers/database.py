import os
import sqlite3

import pyquoks.utils


class DatabaseManager(pyquoks.utils._HasRequiredAttributes):
    """
    Class for managing database connections

    **Required attributes**::

        # Predefined

        _PATH = pyquoks.utils.get_path("db/")

    Attributes:
        _PATH: Path to the directory with databases
    """

    _REQUIRED_ATTRIBUTES = {
        "_PATH",
    }

    _PATH: str = pyquoks.utils.get_path("db/")

    def __init__(self) -> None:
        self._check_attributes()

        os.makedirs(
            name=self._PATH,
            exist_ok=True,
        )

        for attribute, object_type in self.__class__.__annotations__.items():
            if issubclass(object_type, Database):
                setattr(self, attribute, object_type(self))

    def close_all(self) -> None:
        """
        Closes all database connections
        """

        for attribute, object_type in self.__class__.__annotations__.items():
            if issubclass(object_type, Database):
                getattr(self, attribute).close()


class Database(sqlite3.Connection, pyquoks.utils._HasRequiredAttributes):
    """
    Class that represents a database connection

    **Required attributes**::

        _NAME = "users"

        _SQL = f\"""CREATE TABLE IF NOT EXISTS {_NAME} (user_id INTEGER PRIMARY KEY NOT NULL)\"""

        # Predefined

        _FILENAME = "{0}.db"

    Attributes:
        _NAME: Name of the database
        _SQL: SQL expression for creating a table
        _FILENAME: Filename of the database
        _parent: Parent object
    """

    _REQUIRED_ATTRIBUTES = {
        "_NAME",
        "_SQL",
        "_FILENAME",
    }

    _NAME: str

    _SQL: str

    _FILENAME: str = "{0}.db"

    _parent: DatabaseManager

    def __init__(self, parent: DatabaseManager) -> None:
        self._check_attributes()

        self._parent = parent

        self._FILENAME = self._FILENAME.format(self._NAME)

        super().__init__(
            database=self._parent._PATH + self._FILENAME,
            check_same_thread=False,
        )
        self.row_factory = sqlite3.Row

        cursor = self.cursor()

        cursor.execute(
            self._SQL,
        )

        self.commit()
