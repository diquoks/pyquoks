import textwrap

import models
import pyquoks


class DatabaseManager(pyquoks.managers.database.DatabaseManager):
    _PATH = pyquoks.utils.get_path("resources/db/")

    test: TestDatabase


class TestDatabase(pyquoks.managers.database.Database):
    _NAME = "test"

    _SQL = textwrap.dedent(
        f"""\
        CREATE TABLE IF NOT EXISTS {_NAME} (
        id INTEGER PRIMARY KEY NOT NULL,
        test_data TEXT NOT NULL
        )
        """,
    )

    def add_test_data(self, test_data: str) -> models.TestDataModel:
        cursor = self.cursor()

        cursor.execute(
            textwrap.dedent(
                f"""\
                INSERT INTO {self._NAME} (
                test_data
                )
                VALUES (?)
                """,
            ),
            (
                test_data,
            ),
        )

        self.commit()

        cursor.execute(
            textwrap.dedent(
                f"""\
                SELECT * FROM {self._NAME} WHERE rowid == ?
                """,
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
            textwrap.dedent(
                f"""\
                SELECT * FROM {self._NAME} WHERE id == ?
                """,
            ),
            (
                test_data_id,
            ),
        )
        result = cursor.fetchone()

        return models.TestDataModel(**dict(result))
