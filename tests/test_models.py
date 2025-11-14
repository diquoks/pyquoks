from __future__ import annotations
import pyquoks, _test_utils


class TestModels(pyquoks.test.TestBase):
    _MODULE_NAME = __name__

    model = _test_utils.TestModel(
        data={
            "test": "model_test_data",
        }
    )

    models_container = _test_utils.TestModelsContainer(
        data={
            "test": "container_test_data",
            "test_model": {
                "test": "model_test_data",
            }
        }
    )

    list_container = _test_utils.TestListContainer(
        data=[
            {
                "test": "first_test_data",
            },
            {
                "test": "second_test_data",
            }
        ]
    )

    values = _test_utils.TestValues(
        test="values_test_data",
    )

    def test_model(self) -> None:
        self.assert_equal(
            func_name=self.test_model.__name__,
            test_data=self.model.test,
            test_expected="model_test_data",
        )

    def test_container(self) -> None:
        self.assert_equal(
            func_name=self.test_container.__name__,
            test_data=self.models_container.test,
            test_expected="container_test_data",
        )

        self.assert_type(
            func_name=self.test_container.__name__,
            test_data=self.models_container.test_model,
            test_type=_test_utils.TestModel,
        )

        self.assert_equal(
            func_name=self.test_container.__name__,
            test_data=self.models_container.test_model.test,
            test_expected="model_test_data",
        )

        self.assert_type(
            func_name=self.test_container.__name__,
            test_data=self.list_container.test_models,
            test_type=list,
        )

        self.assert_equal(
            func_name=self.test_container.__name__,
            test_data=self.list_container.test_models[0].test,
            test_expected="first_test_data",
        )

        self.assert_equal(
            func_name=self.test_container.__name__,
            test_data=self.list_container.test_models[1].test,
            test_expected="second_test_data",
        )

    def test_values(self) -> None:
        self.assert_equal(
            func_name=self.test_values.__name__,
            test_data=self.values.test,
            test_expected="values_test_data",
        )

        self.values.update(
            test="values_new_data",
        )

        self.assert_equal(
            func_name=self.test_values.__name__,
            test_data=self.values.test,
            test_expected="values_new_data",
        )
