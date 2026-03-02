import os

import PIL.Image

from .providers import assets
from .providers import environment
from .providers import strings


class TestProviders:
    @classmethod
    def setup_class(cls) -> None:
        cls._assets = assets.AssetsProvider()
        cls._environment = environment.EnvironmentProvider()
        cls._strings = strings.StringsProvider()

    def test_assets_provider(self) -> None:
        assert isinstance(
            self._assets.test_images,
            assets.TestImagesDirectory,
        ), "object in the AssetsProvider"
        assert isinstance(self._assets.test_images.test_picture, PIL.Image.Image), "object in the object"

    def test_environment_provider(self) -> None:
        assert self._environment.TEST_VAR is None, "data in the EnvironmentProvider"

        os.environ["TEST_VAR"] = "environment_provider_test_data"

        self._environment.load_variables()

        assert self._environment.TEST_VAR == "environment_provider_test_data", "updated data in the EnvironmentProvider"

    def test_strings_provider(self) -> None:
        assert isinstance(self._strings.test, strings.TestStrings), "object in the StringsProvider"
        assert self._strings.test.test_string == "strings_provider_test_data", "data in the object"
