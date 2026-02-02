import pyquoks


class ConfigManager(pyquoks.managers.config.ConfigManager):
    _PATH = pyquoks.utils.get_path("resources/config_manager_test.ini")

    test: TestConfig


class TestConfig(pyquoks.managers.config.Config):
    _SECTION = "Test"

    _VALUES = {
        "test_str": str,
        "test_bool": bool,
        "test_int": int,
        "test_float": float,
        "test_dict": dict,
        "test_list": list,
    }

    test_str: str
    test_bool: bool
    test_int: int
    test_float: float
    test_dict: dict
    test_list: list
