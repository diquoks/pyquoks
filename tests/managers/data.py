import tests.models
import pyquoks


class DataManager(pyquoks.managers.data.DataManager):
    _PATH = pyquoks.utils.get_path("resources/data/")

    test_list: list[tests.models.TestModel]
    test_model: tests.models.TestModel
