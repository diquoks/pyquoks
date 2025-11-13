from __future__ import annotations
import pyquoks


class TestModel(pyquoks.models.Model):
    _ATTRIBUTES = {
        "test",
    }

    test: str


class TestModelsContainer(pyquoks.models.Container):
    _ATTRIBUTES = {
        "test",
    }

    _OBJECTS = {
        "test_model": TestModel,
    }

    test: str
    test_model: TestModel


class TestListContainer(pyquoks.models.Container):
    _DATA = {
        "test_models": TestModel,
    }

    test_models: list[TestModel]


class TestValues(pyquoks.models.Values):
    _ATTRIBUTES = {
        "test",
    }

    test: str


class TestModels(pyquoks.test.TestBase):
    _MODULE_NAME = __name__

    def test_model(self) -> None:
        model = TestModel(
            data={
                "test": "model_test_data",
            }
        )

        self.assert_is(
            func_name=self.test_model.__name__,
            test_data=model.test,
            test_expected="model_test_data",
        )

    def test_container(self) -> None:
        models_container = TestModelsContainer(
            data={
                "test": "container_test_data",
                "test_model": {
                    "test": "model_test_data",
                }
            }
        )

        self.assert_is(
            func_name=self.test_container.__name__,
            test_data=models_container.test,
            test_expected="container_test_data",
        )

        self.assert_is(
            func_name=self.test_container.__name__,
            test_data=models_container.test_model.test,
            test_expected="model_test_data",
        )

        list_container = TestListContainer(
            data=[
                {
                    "test": "first_test_data",
                },
                {
                    "test": "second_test_data",
                }
            ]
        )

        self.assert_is(
            func_name=self.test_container.__name__,
            test_data=list_container.test_models[0].test,
            test_expected="first_test_data",
        )

        self.assert_is(
            func_name=self.test_container.__name__,
            test_data=list_container.test_models[1].test,
            test_expected="second_test_data",
        )

    def test_values(self) -> None:
        values = TestValues(
            test="values_test_data",
        )

        self.assert_is(
            func_name=self.test_values.__name__,
            test_data=values.test,
            test_expected="values_test_data",
        )

        values.update(
            test="values_new_data",
        )

        self.assert_is(
            func_name=self.test_values.__name__,
            test_data=values.test,
            test_expected="values_new_data",
        )
