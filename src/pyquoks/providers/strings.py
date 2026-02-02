class StringsProvider:
    """
    Class for providing various strings data
    """

    def __init__(self) -> None:
        for attribute, child_class in self.__class__.__annotations__.items():
            if issubclass(child_class, Strings):
                setattr(self, attribute, child_class(self))
            else:
                raise AttributeError(
                    f"{attribute} has incorrect type! (must be subclass of {Strings.__name__})",
                )


class Strings:
    """
    Class that represents a container for strings
    """

    # noinspection PyUnusedLocal
    def __init__(self, parent: StringsProvider) -> None:
        ...  # TODO
