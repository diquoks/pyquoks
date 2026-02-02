import shutil

import managers
import models
import pyquoks


class TestManagers(pyquoks.test.TestCase):
    _MODULE_NAME = __name__

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._config = managers.config.ConfigManager()
        cls._data = managers.data.DataManager()
        cls._database = managers.database.DatabaseManager()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

        shutil.rmtree(
            path=cls._database._PATH,
        )

    def test_config_manager(self) -> None:
        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config.test.test_str,
            test_expected="config_manager_test_data",
            message="str data in the ConfigManager",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config.test.test_bool,
            test_expected=False,
            message="bool data in the ConfigManager",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config.test.test_int,
            test_expected=16,
            message="int data in the ConfigManager",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config.test.test_float,
            test_expected=1.025,
            message="float data in the ConfigManager",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config.test.test_dict,
            test_expected={"test": "config_manager_test_data"},
            message="dict data in the ConfigManager",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config.test.test_list,
            test_expected=["config_manager_test_data"],
            message="list data in the ConfigManager",
        )

        self._config.test.update(
            test_str="config_manager_new_data",
            test_bool=True,
            test_int=32,
            test_float=1.075,
            test_dict={"test": "config_manager_new_data"},
            test_list=["config_manager_new_data"],
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config.test.test_str,
            test_expected="config_manager_new_data",
            message="updated str data in the ConfigManager",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config.test.test_bool,
            test_expected=True,
            message="updated bool data in the ConfigManager",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config.test.test_int,
            test_expected=32,
            message="updated int data in the ConfigManager",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config.test.test_float,
            test_expected=1.075,
            message="updated float data in the ConfigManager",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config.test.test_dict,
            test_expected={"test": "config_manager_new_data"},
            message="updated dict data in the ConfigManager",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config.test.test_list,
            test_expected=["config_manager_new_data"],
            message="updated list data in the ConfigManager",
        )

        self._config.test.update(
            test_str="config_manager_test_data",
            test_bool=False,
            test_int=16,
            test_float=1.025,
            test_dict={"test": "config_manager_test_data"},
            test_list=["config_manager_test_data"],
        )

    def test_data_manager(self) -> None:
        self.assert_type(
            func_name=self.test_data_manager.__name__,
            test_data=self._data.test_list,
            test_type=list,
            message="list in the DataManager",
        )

        self.assert_type(
            func_name=self.test_data_manager.__name__,
            test_data=self._data.test_list[0],
            test_type=models.TestModel,
            message="object in the list",
        )

        self.assert_type(
            func_name=self.test_data_manager.__name__,
            test_data=self._data.test_model,
            test_type=models.TestModel,
            message="object in the DataManager",
        )

        self._data.update(
            test_model=models.TestModel(
                test="model_new_data",
            ),
        )

        self.assert_equal(
            func_name=self.test_data_manager.__name__,
            test_data=self._data.test_model.test,
            test_expected="model_new_data",
            message="updated data in the DataManager",
        )

        self._data.update(
            test_model=models.TestModel(
                test="model_test_data",
            )
        )

        self._data.update(
            test_list=[
                models.TestModel(
                    test="list_new_data",
                ),
            ],
        )

        self.assert_equal(
            func_name=self.test_data_manager.__name__,
            test_data=self._data.test_list[0].test,
            test_expected="list_new_data",
            message="updated data in the DataManager",
        )

        self._data.update(
            test_list=[
                models.TestModel(
                    test="list_test_data",
                ),
            ],
        )

    def test_database_manager(self) -> None:
        current_test_data = self._database.test.add_test_data(
            test_data="database_manager_test_data",
        )

        self.assert_type(
            func_name=self.test_database_manager.__name__,
            test_data=current_test_data,
            test_type=models.TestDataModel,
            message="DatabaseManager creates object from added data",
        )

        current_test_data = self._database.test.get_test_data(
            test_data_id=current_test_data.id,
        )

        self.assert_type(
            func_name=self.test_database_manager.__name__,
            test_data=current_test_data,
            test_type=models.TestDataModel,
            message="DatabaseManager creates object from requested data",
        )

        self.assert_equal(
            func_name=self.test_database_manager.__name__,
            test_data=current_test_data.test_data,
            test_expected="database_manager_test_data",
            message="data in the created object",
        )

        self._database.close_all()
