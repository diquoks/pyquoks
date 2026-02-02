import os

import PIL.Image

import providers
import pyquoks


class TestProviders(pyquoks.test.TestCase):
    _MODULE_NAME = __name__

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._assets = providers.assets.AssetsProvider()
        cls._environment = providers.environment.EnvironmentProvider()
        cls._strings = providers.strings.StringsProvider()

    def test_assets_provider(self) -> None:
        self.assert_type(
            func_name=self.test_assets_provider.__name__,
            test_data=self._assets.test_images,
            test_type=providers.assets.TestImagesDirectory,
            message="object in the AssetsProvider",
        )

        self.assert_type(
            func_name=self.test_assets_provider.__name__,
            test_data=self._assets.test_images.test_picture,
            test_type=PIL.Image.Image,
            message="object in the object",
        )

    def test_environment_provider(self) -> None:
        self.assert_equal(
            func_name=self.test_environment_provider.__name__,
            test_data=self._environment.TEST_VAR,
            test_expected=None,
            message="data in the EnvironmentProvider",
        )

        os.environ["TEST_VAR"] = "environment_provider_test_data"

        self._environment.load_variables()

        self.assert_equal(
            func_name=self.test_environment_provider.__name__,
            test_data=self._environment.TEST_VAR,
            test_expected="environment_provider_test_data",
            message="updated data in the EnvironmentProvider",
        )

    def test_strings_provider(self) -> None:
        self.assert_type(
            func_name=self.test_strings_provider.__name__,
            test_data=self._strings.test,
            test_type=providers.strings.TestStrings,
            message="object in the StringsProvider",
        )

        self.assert_equal(
            func_name=self.test_strings_provider.__name__,
            test_data=self._strings.test.test_string,
            test_expected="strings_provider_test_data",
            message="data in the object",
        )
