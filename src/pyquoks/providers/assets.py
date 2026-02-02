import io

import PIL.Image
import requests

import pyquoks.utils


class AssetsProvider(pyquoks.utils._HasRequiredAttributes):
    """
    Class for providing various assets data

    **Required attributes**::

        # Predefined:

        _PATH = pyquoks.utils.get_path("assets/")

    Attributes:
        _PATH: Path to the directory with assets folders
    """

    _REQUIRED_ATTRIBUTES = {
        "_PATH",
    }

    _PATH: str = pyquoks.utils.get_path("assets/")

    def __init__(self) -> None:
        self._check_attributes()

        for attribute, object_type in self.__class__.__annotations__.items():
            if issubclass(object_type, Directory | Network):
                setattr(self, attribute, object_type(self))


class Directory(pyquoks.utils._HasRequiredAttributes):
    """
    Class that represents a directory with various assets

    **Required attributes**::

        _ATTRIBUTES = {"picture1", "picture2"}

        _PATH = "images/"

        _FILENAME = "{0}.png"

    Attributes:
        _ATTRIBUTES: Names of files in the directory
        _PATH: Path to the directory with assets files
        _FILENAME: Filename of assets files
        _parent: Parent object
    """

    _REQUIRED_ATTRIBUTES = {
        "_ATTRIBUTES",
        "_PATH",
        "_FILENAME",
    }

    _ATTRIBUTES: set[str]

    _PATH: str

    _FILENAME: str

    _parent: AssetsProvider

    def __init__(self, parent: AssetsProvider) -> None:
        self._check_attributes()

        self._parent = parent

        self._PATH = self._parent._PATH + self._PATH

        for attribute in self._ATTRIBUTES:
            try:
                setattr(self, attribute, self.file_image(
                    path=self._PATH + self._FILENAME.format(attribute),
                ))
            except Exception:
                setattr(self, attribute, None)

    @staticmethod
    def file_image(path: str) -> PIL.Image.Image:
        """
        :param path: Absolute path of the image file
        :return: Image object from a file
        """

        with open(path, "rb") as file:
            return PIL.Image.open(
                fp=io.BytesIO(file.read()),
            )


class Network(pyquoks.utils._HasRequiredAttributes):
    """
    Class that represents a set of images obtained from a network

    **Required attributes**::

        _URLS = {"example": "https://example.com/image.png"}

    Attributes:
        _URLS: Dictionary with names of attributes and URLs
        _parent: Parent object
    """

    _REQUIRED_ATTRIBUTES = {
        "_URLS",
    }

    _URLS: dict[str, str]

    _parent: AssetsProvider

    def __init__(self, parent: AssetsProvider) -> None:
        self._check_attributes()

        self._parent = parent

        for attribute, url in self._URLS.items():
            try:
                setattr(self, attribute, self.network_image(
                    url=url,
                ))
            except Exception:
                setattr(self, attribute, None)

    @staticmethod
    def network_image(url: str) -> PIL.Image.Image:
        """
        :param url: URL of the image file
        :return: Image object from a URL
        """

        return PIL.Image.open(
            fp=io.BytesIO(requests.get(url).content),
        )
