import pyquoks.managers.database
import pyquoks.utils
from .. import models


class DatabaseManager(pyquoks.managers.database.DatabaseManager):
    _PATH = pyquoks.utils.get_path("resources/db/")

    test: TestDatabase


class TestDatabase(pyquoks.managers.database.Database):
    _NAME = "test"

    _SQL = pyquoks.utils.format_multiline_string(
        """
        CREATE TABLE IF NOT EXISTS {0} (
        id INTEGER PRIMARY KEY NOT NULL,
        test_data TEXT NOT NULL
        )
        """,
        _NAME,
    )

    def add_test_data(self, test_data: str) -> models.TestDataModel:
        cursor = self.cursor()

        cursor.execute(
            pyquoks.utils.format_multiline_string(
                """
                INSERT INTO {0} (
                test_data
                )
                VALUES (?)
                """,
                self._NAME,
            ),
            (
                test_data,
            ),
        )

        self.commit()

        cursor.execute(
            pyquoks.utils.format_multiline_string(
                """
                SELECT * FROM {0} WHERE rowid == ?
                """,
                self._NAME,
            ),
            (
                cursor.lastrowid,
            ),
        )
        result = cursor.fetchone()

        return models.TestDataModel(**dict(result))

    def get_test_data(self, test_data_id: int) -> models.TestDataModel:
        cursor = self.cursor()

        cursor.execute(
            pyquoks.utils.format_multiline_string(
                """
                SELECT * FROM {0} WHERE id == ?
                """,
                self._NAME,
            ),
            (
                test_data_id,
            ),
        )
        result = cursor.fetchone()

        return models.TestDataModel(**dict(result))
