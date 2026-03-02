import shutil

from . import models
from .managers import config
from .managers import database


class TestManagers:
    @classmethod
    def setup_class(cls) -> None:
        cls._config = config.ConfigManager()
        cls._database = database.DatabaseManager()

    @classmethod
    def teardown_class(cls) -> None:
        shutil.rmtree(
            path=cls._database._PATH,
        )

    def test_config_manager(self) -> None:
        assert self._config.test.test_str == "config_manager_test_data", "str data in the ConfigManager"
        assert self._config.test.test_bool == False, "bool data in the ConfigManager"
        assert self._config.test.test_int == 16, "int data in the ConfigManager"
        assert self._config.test.test_float == 1.025, "float data in the ConfigManager"
        assert self._config.test.test_dict == {"test": "config_manager_test_data"}, "dict data in the ConfigManager"
        assert self._config.test.test_list == ["config_manager_test_data"], "list data in the ConfigManager"

        self._config.test.update(
            test_str="config_manager_new_data",
            test_bool=True,
            test_int=32,
            test_float=1.075,
            test_dict={"test": "config_manager_new_data"},
            test_list=["config_manager_new_data"],
        )

        assert self._config.test.test_str == "config_manager_new_data", "updated str data in the ConfigManager"
        assert self._config.test.test_bool == True, "updated bool data in the ConfigManager"
        assert self._config.test.test_int == 32, "updated int data in the ConfigManager"
        assert self._config.test.test_float == 1.075, "updated float data in the ConfigManager"
        assert self._config.test.test_dict == {
            "test": "config_manager_new_data"
        }, "updated dict data in the ConfigManager"
        assert self._config.test.test_list == ["config_manager_new_data"], "updated list data in the ConfigManager"

        self._config.test.update(
            test_str="config_manager_test_data",
            test_bool=False,
            test_int=16,
            test_float=1.025,
            test_dict={"test": "config_manager_test_data"},
            test_list=["config_manager_test_data"],
        )

    def test_database_manager(self) -> None:
        current_test_data = self._database.test.add_test_data(
            test_data="database_manager_test_data",
        )

        assert isinstance(
            current_test_data,
            models.TestDataModel,
        ), "DatabaseManager creates object from added data"

        current_test_data = self._database.test.get_test_data(
            test_data_id=current_test_data.id,
        )

        assert isinstance(
            current_test_data,
            models.TestDataModel,
        ), "DatabaseManager creates object from requested data"
        assert current_test_data.test_data == "database_manager_test_data", "data in the created object"

        self._database.close_all()
