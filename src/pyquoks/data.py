from __future__ import annotations
import configparser, datetime, logging, json, sys, io, os
import requests, PIL.Image, PIL.ImageDraw
from . import utils


# region Providers

class IDataProvider:
    """
    Class for reading and storing data from ``.json`` files
    """

    _PATH: str = None
    """
    Path to the directory with ``.json`` files

    Example:
        _PATH = "data/{0}.json"
    """

    _DATA_VALUES: dict[str, type]
    """
    Dictionary with filenames and containers

    Example:
        _DATA_VALUES = {"users": UsersContainer}
    """

    def __init__(self) -> None:
        for filename, container in self._DATA_VALUES.items():
            try:
                with open(self._PATH.format(filename), "rb") as file:
                    setattr(self, filename, container(json.loads(file.read())))
            except:
                setattr(self, filename, None)


class IConfigProvider:
    """
    Class for reading and storing data from ``.ini`` files
    """

    class IConfig:
        """
        Class that represents a section in ``.ini`` file
        """

        _SECTION: str = None
        """
        Name of the section in ``.ini`` file

        Example:
            _SECTION = "Settings"
        """

        _CONFIG_VALUES: dict[str, type]
        """
        Dictionary with settings and their types
        """

        def __init__(self, parent: IConfigProvider = None) -> None:
            if isinstance(parent, IConfigProvider):
                self._CONFIG_VALUES = parent._CONFIG_VALUES.get(self._SECTION)

                self._incorrect_content_exception = configparser.ParsingError("config.ini is filled incorrectly!")
                self._config = configparser.ConfigParser()
                self._config.read(utils.get_path("config.ini"))

                if not self._config.has_section(self._SECTION):
                    self._config.add_section(self._SECTION)

                for settings, data_type in self._CONFIG_VALUES.items():
                    try:
                        setattr(self, settings, self._config.get(self._SECTION, settings))
                    except:
                        self._config.set(self._SECTION, settings, data_type.__name__)
                        with open(utils.get_path("config.ini"), "w", encoding="utf-8") as file:
                            self._config.write(file)

                for settings, data_type in self._CONFIG_VALUES.items():
                    try:
                        if data_type == int:
                            setattr(self, settings, int(getattr(self, settings)))
                        elif data_type == bool:
                            if getattr(self, settings) not in (str(True), str(False)):
                                setattr(self, settings, None)
                                raise self._incorrect_content_exception
                            else:
                                setattr(self, settings, getattr(self, settings) == str(True))
                        elif data_type == dict | list:
                            setattr(self, settings, json.loads(getattr(self, settings)))

                        # TODO: test match-case
                        # match str(data_type):
                        #     case "int":
                        #         setattr(self, settings, int(getattr(self, settings)))
                        #     case "bool":
                        #         if getattr(self, settings) not in (str(True), str(False)):
                        #             setattr(self, settings, None)
                        #             raise self._incorrect_content_exception
                        #         else:
                        #             setattr(self, settings, getattr(self, settings) == str(True))
                        #     case "dict" | "list":
                        #         setattr(self, settings, json.loads(getattr(self, settings)))
                    except:
                        setattr(self, settings, None)
                        raise self._incorrect_content_exception

                if not self.values:
                    raise self._incorrect_content_exception

        @property
        def values(self) -> dict | None:
            """
            :return: Values stored in section
            """

            try:
                return {setting: getattr(self, setting) for setting in self._CONFIG_VALUES.keys()}
            except:
                return None

    _CONFIG_VALUES: dict[str, dict[str, type]]
    """
    Dictionary with sections, their settings and their types

    Example:
        _CONFIG_VALUES = {"Settings": {"version": str}}
    """

    _CONFIG_OBJECTS: dict[str, type]
    """
    Dictionary with names of attributes and child objects

    Example:
        _CONFIG_OBJECTS = {"settings": SettingsConfig}
    """

    def __init__(self) -> None:
        for name, data_class in self._CONFIG_OBJECTS.items():
            setattr(self, name, data_class(self))


class IAssetsProvider:
    class IDirectory:
        """
        Class that represents a directory with various assets
        """

        _PATH: str = None
        """
        Path to the directory with assets files

        Example:
            _PATH = "images/{0}.png"
        """

        _NAMES: set[str]
        """
        Names of files in the directory

        Example:
            _NAMES = {"picture1", "picture2"}
        """

        def __init__(self, parent: IAssetsProvider) -> None:
            if isinstance(parent, IAssetsProvider):
                for filename in self._NAMES:
                    setattr(self, filename, parent.file_image(parent._PATH.format(self._PATH.format(filename))))

    class INetwork:
        """
        Class that represents a set of images obtained from a network
        """

        _URLS: dict[str, str]
        """
        Dictionary with names of attributes and URLs

        Example:
            _URLS = {"example": "https://example.com/image.png"}
        """

        def __init__(self, parent: IAssetsProvider) -> None:
            if isinstance(parent, IAssetsProvider):
                for name, url in self._URLS.items():
                    setattr(self, name, parent.network_image(url))

    _PATH: str
    """
    Path to the directory with assets folders

    Example:
        _PATH = "assets/{0}"
    """

    _ASSETS_OBJECTS: dict[str, type]
    """
    Dictionary with names of attributes and child objects

    Example:
        _ASSETS_OBJECTS = {"images": ImagesAssets, "example": ExampleNetwork}
    """

    def __init__(self) -> None:
        for name, data_class in self._ASSETS_OBJECTS.items():
            setattr(self, name, data_class(self))

    @staticmethod
    def file_image(path: str) -> PIL.Image.Image:
        """
        :return: Image object from a file
        """

        with open(path, "rb") as file:
            return PIL.Image.open(io.BytesIO(file.read()))

    @staticmethod
    def network_image(url: str) -> PIL.Image.Image:
        """
        :return: Image object from a URL
        """

        return PIL.Image.open(io.BytesIO(requests.get(url).content))

    @staticmethod
    def round_corners(image: PIL.Image.Image, radius: int) -> PIL.Image.Image:
        """
        :return: Image with rounded edges of the specified radius
        """

        if image.mode != "RGB":
            image = image.convert("RGB")
        width, height = image.size

        shape = PIL.Image.new("L", (radius * 2, radius * 2), 0)
        PIL.ImageDraw.Draw(shape).ellipse((0, 0, radius * 2, radius * 2), fill=255)

        alpha = PIL.Image.new("L", image.size, "white")
        alpha.paste(shape.crop((0, 0, radius, radius)), (0, 0))
        alpha.paste(shape.crop((0, radius, radius, radius * 2)), (0, height - radius))
        alpha.paste(shape.crop((radius, 0, radius * 2, radius)), (width - radius, 0))
        alpha.paste(shape.crop((radius, radius, radius * 2, radius * 2)), (width - radius, height - radius))
        image.putalpha(alpha)

        return image


class IStringsProvider:
    class IStrings:
        """
        Class that represents a container for strings
        """

        pass

    _STRINGS_OBJECTS: dict[str, type]
    """
    Dictionary with names of attributes and child objects
    """

    def __init__(self) -> None:
        for name, data_class in self._STRINGS_OBJECTS.items():
            setattr(self, name, data_class(self))


# endregion

# region Managers

if sys.platform == "win32":
    import winreg


    class IRegistryManager:
        """
        Class for managing data in the Windows Registry
        """

        class IRegistry:
            """
            Class that represents a key with parameters in the Windows Registry
            """

            _NAME: str = None
            """
            Name of key in the Windows Registry

            Example:
                _NAME = "OAuth"
            """

            _REGISTRY_VALUES: dict[str, int]
            """
            Dictionary with settings and their types
            """

            _path: winreg.HKEYType

            def __init__(self, parent: IRegistryManager = None) -> None:
                if isinstance(parent, IRegistryManager):
                    self._REGISTRY_VALUES = parent._REGISTRY_VALUES.get(self._NAME)
                    self._path = winreg.CreateKey(parent._path, self._NAME)

                    for setting in self._REGISTRY_VALUES.keys():
                        try:
                            setattr(self, setting, winreg.QueryValueEx(self._path, setting)[int()])
                        except:
                            setattr(self, setting, None)

            @property
            def values(self) -> dict | None:
                """
                :return: Values stored in key in the Windows Registry
                """

                try:
                    return {setting: getattr(self, setting) for setting in self._REGISTRY_VALUES.keys()}
                except:
                    return None

            def refresh(self) -> IRegistryManager.IRegistry:
                """
                :return: Instance with refreshed values
                """

                self.__init__()
                return self

            def update(self, **kwargs) -> None:
                """
                Updates provided settings in the Windows Registry
                """

                for setting, value in kwargs.items():
                    winreg.SetValueEx(self._path, setting, None, self._REGISTRY_VALUES.get(setting), value)
                    setattr(self, setting, value)

        _KEY: str
        """
        Path to key in the Windows Registry

        Example:
            _KEY = "Software\\\\\\\\diquoks Software\\\\\\\\pyquoks"
        """

        _REGISTRY_VALUES: dict[str, dict[str, int]]
        """
        Dictionary with keys, their settings and their types

        Example:
            _REGISTRY_VALUES = {"OAuth": {"access_token": winreg.REG_SZ}}
        """

        _REGISTRY_OBJECTS: dict[str, type]
        """
        Dictionary with names of attributes and child objects

        Example:
            _REGISTRY_OBJECTS = {"oauth": OAuthRegistry}
        """

        _path: winreg.HKEYType

        def __init__(self) -> None:
            self._path = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self._KEY)

            for name, data_class in self._REGISTRY_OBJECTS.items():
                setattr(self, name, data_class(self))

        def refresh(self) -> IRegistryManager:
            """
            :return: Instance with refreshed values
            """

            self.__init__()
            return self


# endregion

# region Services

class LoggerService(logging.Logger):
    """
    Class that provides methods for parallel logging
    """

    def __init__(
            self,
            name: str, file_handling: bool = True,
            filename: str = datetime.datetime.now().strftime("%d-%m-%y-%H-%M-%S"),
            level: int = logging.NOTSET,
            folder_name: str = "logs",
    ) -> None:
        super().__init__(name, level)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(
            logging.Formatter(
                fmt="$levelname $asctime $name - $message",
                datefmt="%d-%m-%y %H:%M:%S",
                style="$",
            )
        )
        self.addHandler(stream_handler)

        if file_handling:
            os.makedirs(utils.get_path(folder_name, only_abspath=True), exist_ok=True)

            file_handler = logging.FileHandler(
                utils.get_path(f"{folder_name}/{filename}-{name}.log", only_abspath=True),
                encoding="utf-8",
            )
            file_handler.setFormatter(
                logging.Formatter(
                    fmt="$levelname $asctime - $message",
                    datefmt="%d-%m-%y %H:%M:%S",
                    style="$",
                ),
            )
            self.addHandler(file_handler)

    def log_exception(self, e: Exception) -> None:
        """
        Logs an exception with detailed traceback
        """

        self.error(msg=e, exc_info=True)

# endregion
