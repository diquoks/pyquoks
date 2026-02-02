import json
import os
import typing

import pydantic

import pyquoks.utils


class DataManager(pyquoks.utils._HasRequiredAttributes):
    """
    Class for managing data from JSON-like files

    **Required attributes**::

        # Predefined:

        _PATH = pyquoks.utils.get_path("data/")

        _FILENAME = "{0}.json"

    Attributes:
        _PATH: Path to the directory with JSON-like files
        _FILENAME: Filename of JSON-like files
    """

    _REQUIRED_ATTRIBUTES = {
        "_PATH",
        "_FILENAME",
    }

    _PATH: str = pyquoks.utils.get_path("data/")

    _FILENAME: str = "{0}.json"

    def __init__(self) -> None:
        self._check_attributes()

        for attribute, object_type in self.__class__.__annotations__.items():
            if issubclass(
                    typing.get_args(object_type)[0],
                    pydantic.BaseModel,
            ) if typing.get_origin(object_type) else issubclass(
                object_type,
                pydantic.BaseModel,
            ):
                try:
                    with open(self._PATH + self._FILENAME.format(attribute), "rb") as file:
                        data = json.loads(file.read())

                        if typing.get_origin(object_type) == list:
                            setattr(self, attribute, [typing.get_args(object_type)[0](**model) for model in data])
                        else:
                            setattr(self, attribute, object_type(**data))
                except Exception:
                    setattr(self, attribute, None)
            else:
                raise AttributeError(
                    f"{attribute} has incorrect type! (must be subclass of {pydantic.BaseModel.__name__} or {list.__name__} of its subclasses)",
                )

    def update(self, **kwargs) -> None:
        """
        Updates provided attributes in object
        """

        for attribute, value in kwargs.items():
            value: pydantic.BaseModel | list[pydantic.BaseModel]

            if attribute not in self.__class__.__annotations__.keys():
                raise AttributeError(f"{attribute} is not specified!")

            object_type = self.__class__.__annotations__.get(attribute)

            if not isinstance(
                    value,
                    typing.get_origin(object_type) if typing.get_origin(object_type) else object_type,
            ):
                raise AttributeError(
                    f"{attribute} has incorrect type! (must be {object_type.__name__})",
                )

            setattr(self, attribute, value)

            os.makedirs(
                name=self._PATH,
                exist_ok=True,
            )

            with open(self._PATH + self._FILENAME.format(attribute), "w", encoding="utf-8") as file:
                json.dump(
                    [model.model_dump() for model in value] if typing.get_origin(
                        object_type,
                    ) == list else value.model_dump(),
                    fp=file,
                    ensure_ascii=False,
                    indent=2,
                )
