from __future__ import annotations
import shutil
import PIL.Image
import pyquoks, _test_utils


class TestData(pyquoks.test.TestCase):
    _MODULE_NAME = __name__

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._data_provider = _test_utils.DataProvider()
        cls._assets_provider = _test_utils.AssetsProvider()
        cls._strings_provider = _test_utils.StringsProvider()
        cls._config_manager = _test_utils.ConfigManager()
        cls._database_manager = _test_utils.DatabaseManager()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(
            path=cls._database_manager._PATH,
        )

    def test_data_provider(self) -> None:
        self.assert_type(
            func_name=self.test_data_provider.__name__,
            test_data=self._data_provider.test_list,
            test_type=_test_utils.TestListContainer,
        )

        self.assert_type(
            func_name=self.test_data_provider.__name__,
            test_data=self._data_provider.test_models,
            test_type=_test_utils.TestModelsContainer,
        )

    def test_assets_provider(self) -> None:
        self.assert_type(
            func_name=self.test_assets_provider.__name__,
            test_data=self._assets_provider.test_images,
            test_type=_test_utils.AssetsProvider.TestImagesDirectory,
        )

        self.assert_type(
            func_name=self.test_assets_provider.__name__,
            test_data=self._assets_provider.test_images.test_picture,
            test_type=PIL.Image.Image,
        )

    def test_strings_provider(self) -> None:
        self.assert_type(
            func_name=self.test_strings_provider.__name__,
            test_data=self._strings_provider.test,
            test_type=_test_utils.StringsProvider.TestStrings,
        )

        self.assert_equal(
            func_name=self.test_strings_provider.__name__,
            test_data=self._strings_provider.test.test_string,
            test_expected="strings_provider_test_data",
        )

    def test_config_manager(self) -> None:
        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config_manager.test.test_str,
            test_expected="config_manager_test_data",
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config_manager.test.test_bool,
            test_expected=False,
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config_manager.test.test_int,
            test_expected=16,
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config_manager.test.test_float,
            test_expected=1.025,
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config_manager.test.test_dict,
            test_expected={"test": "config_manager_test_data"},
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config_manager.test.test_list,
            test_expected=["config_manager_test_data"],
        )

        self._config_manager.test.update(
            test_str="config_manager_new_data"
        )

        self.assert_equal(
            func_name=self.test_config_manager.__name__,
            test_data=self._config_manager.test.test_str,
            test_expected="config_manager_new_data",
        )

        self._config_manager.test.update(
            test_str="config_manager_test_data"
        )

    def test_database_manager(self) -> None:
        current_test_data = self._database_manager.test.add_test_data(
            test_data="database_manager_test_data",
        )

        self.assert_type(
            func_name=self.test_database_manager.__name__,
            test_data=current_test_data,
            test_type=_test_utils.TestDataModel,
        )

        current_test_data = self._database_manager.test.get_test_data(
            test_data_id=current_test_data.id,
        )

        self.assert_type(
            func_name=self.test_database_manager.__name__,
            test_data=current_test_data,
            test_type=_test_utils.TestDataModel,
        )

        self.assert_equal(
            func_name=self.test_database_manager.__name__,
            test_data=current_test_data.test_data,
            test_expected="database_manager_test_data",
        )

        self._database_manager.close_all()
