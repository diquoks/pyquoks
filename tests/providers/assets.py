import PIL.Image

import pyquoks.providers.assets


class AssetsProvider(pyquoks.providers.assets.AssetsProvider):
    _PATH = pyquoks.utils.get_path("resources/assets/")

    test_images: TestImagesDirectory


class TestImagesDirectory(pyquoks.providers.assets.Directory):
    _PATH = "test_images/"

    _FILENAMES = {
        "test_picture.png",
    }

    test_picture: PIL.Image.Image
