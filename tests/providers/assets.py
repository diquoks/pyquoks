import PIL.Image

import pyquoks


class AssetsProvider(pyquoks.providers.assets.AssetsProvider):
    _PATH = pyquoks.utils.get_path("resources/assets/")

    test_images: TestImagesDirectory


class TestImagesDirectory(pyquoks.providers.assets.Directory):
    _ATTRIBUTES = {
        "test_picture",
    }

    _PATH = "test_images/"

    _FILENAME = "{0}.png"

    test_picture: PIL.Image.Image
