import shutil

import PIL.Image

import _test_utils
import pyquoks


class TestData(pyquoks.test.TestCase):
    _MODULE_NAME = __name__

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._assets_provider = _test_utils.AssetsProvider()
        cls._strings_provider = _test_utils.StringsProvider()
        cls._config_manager = _test_utils.ConfigManager()
        cls._data_manager = _test_utils.DataManager()
        cls._database_manager = _test_utils.DatabaseManager()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(
            path=cls._database_manager._PATH,
        )

    def test_assets_provider(self) -> None:
        self.assert_type(
            func_name=self.test_assets_provider.__name__,
            test_data=self._assets_provider.test_images,
            test_type=_test_utils.AssetsProvider.TestImagesDirectory,
            message="object in the AssetsProvider",
        )

        self.assert_type(
            func_name=self.test_assets_provider.__name__,
            test_data=self._assets_provider.test_images.test_picture,
            test_type=PIL.Image.Image,
            message="object in the object",
        )

    def test_strings_provider(self) -> None:
        self.assert_type(
            func_name=self.test_strings_provider.__name__,
            test_data=self._strings_provider.test,
            test_type=_test_utils.StringsProvider.TestStrings,
            message="object in the StringsProvider",
        )

        self.assert_equal(
            func_name=self.test_strings_provider.__name__,
            test_data=self._strings_provider.test.test_string,
            test_expected="strings_provider_test_data",
            message="data in the object",
        )

    def test_config_manager(self) -> None:
        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config_manager.test.test_str,
            test_expected="config_manager_test_data",
            message="str data in the ConfigManager",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config_manager.test.test_bool,
            test_expected=False,
            message="bool data in the ConfigManager",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config_manager.test.test_int,
            test_expected=16,
            message="int data in the ConfigManager",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config_manager.test.test_float,
            test_expected=1.025,
            message="float data in the ConfigManager",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config_manager.test.test_dict,
            test_expected={"test": "config_manager_test_data"},
            message="dict data in the ConfigManager",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config_manager.test.test_list,
            test_expected=["config_manager_test_data"],
            message="list data in the ConfigManager",
        )

        self._config_manager.test.update(
            test_str="config_manager_new_data",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config_manager.test.test_str,
            test_expected="config_manager_new_data",
            message="updated data in the ConfigManager",
        )

        self._config_manager.test.update(
            test_str="config_manager_test_data",
        )

    def test_data_manager(self) -> None:
        self.assert_type(
            func_name=self.test_data_manager.__name__,
            test_data=self._data_manager.test_list,
            test_type=list,
            message="list in the DataManager",
        )

        self.assert_type(
            func_name=self.test_data_manager.__name__,
            test_data=self._data_manager.test_list[0],
            test_type=_test_utils.TestModel,
            message="object in the list",
        )

        self.assert_type(
            func_name=self.test_data_manager.__name__,
            test_data=self._data_manager.test_model,
            test_type=_test_utils.TestModel,
            message="object in the DataManager",
        )

        self._data_manager.update(
            test_model=_test_utils.TestModel(
                test="model_new_data",
            ),
        )

        self.assert_equal(
            func_name=self.test_data_manager.__name__,
            test_data=self._data_manager.test_model.test,
            test_expected="model_new_data",
            message="updated data in the DataManager",
        )

        self._data_manager.update(
            test_model=_test_utils.TestModel(
                test="model_test_data",
            )
        )

        self._data_manager.update(
            test_list=[
                _test_utils.TestModel(
                    test="list_new_data",
                ),
            ],
        )

        self.assert_equal(
            func_name=self.test_data_manager.__name__,
            test_data=self._data_manager.test_list[0].test,
            test_expected="list_new_data",
            message="updated data in the DataManager",
        )

        self._data_manager.update(
            test_list=[
                _test_utils.TestModel(
                    test="list_test_data",
                ),
            ],
        )

    def test_database_manager(self) -> None:
        current_test_data = self._database_manager.test.add_test_data(
            test_data="database_manager_test_data",
        )

        self.assert_type(
            func_name=self.test_database_manager.__name__,
            test_data=current_test_data,
            test_type=_test_utils.TestDataModel,
            message="DatabaseManager creates object from added data",
        )

        current_test_data = self._database_manager.test.get_test_data(
            test_data_id=current_test_data.id,
        )

        self.assert_type(
            func_name=self.test_database_manager.__name__,
            test_data=current_test_data,
            test_type=_test_utils.TestDataModel,
            message="DatabaseManager creates object from requested data",
        )

        self.assert_equal(
            func_name=self.test_database_manager.__name__,
            test_data=current_test_data.test_data,
            test_expected="database_manager_test_data",
            message="data in the created object",
        )

        self._database_manager.close_all()
