import models
import pyquoks


class DataManager(pyquoks.managers.data.DataManager):
    _PATH = pyquoks.utils.get_path("resources/data/")

    test_list: list[models.TestModel]
    test_model: models.TestModel
