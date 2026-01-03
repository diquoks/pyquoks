import textwrap
import typing

import PIL.Image
import pydantic

import src.pyquoks


# region models.py

class TestModel(pydantic.BaseModel):
    test: str


class TestDataModel(pydantic.BaseModel):
    id: int
    test_data: str


# endregion

# region data.py

class AssetsProvider(src.pyquoks.data.AssetsProvider):
    class TestImagesDirectory(src.pyquoks.data.AssetsProvider.Directory):
        _ATTRIBUTES = {
            "test_picture",
        }

        _PATH = "test_images/"

        _FILENAME = "{0}.png"

        test_picture: PIL.Image.Image

    _PATH = src.pyquoks.utils.get_path("tests/resources/assets/")

    test_images: TestImagesDirectory


class StringsProvider(src.pyquoks.data.StringsProvider):
    class TestStrings(src.pyquoks.data.StringsProvider.Strings):
        @property
        def test_string(self) -> str:
            return "strings_provider_test_data"

    test: TestStrings


class ConfigManager(src.pyquoks.data.ConfigManager):
    class TestConfig(src.pyquoks.data.ConfigManager.Config):
        _SECTION = "Test"

        _VALUES = {
            "test_str": str,
            "test_bool": bool,
            "test_int": int,
            "test_float": float,
            "test_dict": dict,
            "test_list": list,
        }

        test_str: str
        test_bool: bool
        test_int: int
        test_float: float
        test_dict: dict
        test_list: list

    _PATH = src.pyquoks.utils.get_path("tests/resources/config_manager_test.ini")

    test: TestConfig


class DataManager(src.pyquoks.data.DataManager):
    _PATH = src.pyquoks.utils.get_path("tests/resources/data/")

    test_list: list[TestModel]
    test_model: TestModel


class DatabaseManager(src.pyquoks.data.DatabaseManager):
    class TestDatabase(src.pyquoks.data.DatabaseManager.Database):
        _NAME = "test"

        _SQL = textwrap.dedent(
            f"""\
            CREATE TABLE IF NOT EXISTS {_NAME} (
            id INTEGER PRIMARY KEY NOT NULL,
            test_data TEXT NOT NULL
            )
            """,
        )

        def add_test_data(self, test_data: str) -> TestDataModel:
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

            return TestDataModel(**dict(result))

        def get_test_data(self, test_data_id: int) -> TestDataModel:
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

            return TestDataModel(**dict(result))

    _PATH = src.pyquoks.utils.get_path("tests/resources/db/")

    test: TestDatabase


# endregion

# region utils.py

def raise_test_exception() -> typing.NoReturn:
    raise NotImplementedError

# endregion
