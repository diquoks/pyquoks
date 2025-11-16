from __future__ import annotations
import PIL.Image
import pyquoks


# region models.py

class TestModel(pyquoks.models.Model):
    _ATTRIBUTES = {
        "test",
    }

    test: str


class TestDataModel(pyquoks.models.Model):
    _ATTRIBUTES = {
        "id",
        "test_data",
    }

    id: int
    test_data: str


class TestModelsContainer(pyquoks.models.Container):
    _ATTRIBUTES = {
        "test",
    }

    _OBJECTS = {
        "test_model": TestModel,
    }

    test: str
    test_model: TestModel


class TestListContainer(pyquoks.models.Container):
    _DATA = {
        "test_models": TestModel,
    }

    test_models: list[TestModel]


class TestValues(pyquoks.models.Values):
    _ATTRIBUTES = {
        "test",
    }

    test: str


# endregion

# region data.py

class DataProvider(pyquoks.data.DataProvider):
    _OBJECTS = {
        "test_list": TestListContainer,
        "test_models": TestModelsContainer,
    }

    _PATH = pyquoks.utils.get_path("resources/data/")

    test_list: TestListContainer
    test_models: TestModelsContainer


class AssetsProvider(pyquoks.data.AssetsProvider):
    class TestImagesDirectory(pyquoks.data.AssetsProvider.Directory):
        _ATTRIBUTES = {
            "test_picture",
        }

        _PATH = "test_images/"

        _FILENAME = "{0}.png"

        test_picture: PIL.Image.Image

    _OBJECTS = {
        "test_images": TestImagesDirectory,
    }

    _PATH = pyquoks.utils.get_path("resources/assets/")

    test_images: TestImagesDirectory


class StringsProvider(pyquoks.data.StringsProvider):
    class TestStrings(pyquoks.data.StringsProvider.Strings):
        @property
        def test_string(self) -> str:
            return "strings_provider_test_data"

    _OBJECTS = {
        "test": TestStrings,
    }

    test: TestStrings


class ConfigManager(pyquoks.data.ConfigManager):
    class TestConfig(pyquoks.data.ConfigManager.Config):
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

    _OBJECTS = {
        "test": TestConfig,
    }

    _PATH = pyquoks.utils.get_path("resources/config_manager_test.ini")

    test: TestConfig


class DatabaseManager(pyquoks.data.DatabaseManager):
    class TestDatabase(pyquoks.data.DatabaseManager.Database):
        _NAME = "test"

        _SQL = f"""
        CREATE TABLE IF NOT EXISTS {_NAME} (
        id INTEGER PRIMARY KEY NOT NULL,
        test_data TEXT NOT NULL
        )
        """

        def add_test_data(self, test_data: str) -> TestDataModel:
            cursor = self.cursor()

            cursor.execute(
                f"""
                INSERT INTO {self._NAME} (
                test_data
                )
                VALUES (?)
                """,
                (
                    test_data,
                ),
            )

            self.commit()

            cursor.execute(
                f"""
                SELECT * FROM {self._NAME} WHERE rowid == ?
                """,
                (
                    cursor.lastrowid,
                ),
            )
            result = cursor.fetchone()

            return TestDataModel(
                data=dict(result),
            )

        def get_test_data(self, test_data_id: int) -> TestDataModel:
            cursor = self.cursor()

            cursor.execute(
                f"""
                SELECT * FROM {self._NAME} WHERE id == ?
                """,
                (
                    test_data_id,
                ),
            )
            result = cursor.fetchone()

            return TestDataModel(
                data=dict(result),
            )

    _OBJECTS = {
        "test": TestDatabase,
    }

    _PATH = pyquoks.utils.get_path("resources/db/")

    test: TestDatabase

# endregion
