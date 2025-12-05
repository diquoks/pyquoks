from __future__ import annotations

import _test_utils
import pyquoks


class TestModels(pyquoks.test.TestCase):
    _MODULE_NAME = __name__

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._model_data = {
            "test": "model_test_data",
        }
        cls._model = _test_utils.TestModel(
            data=cls._model_data,
        )

        cls._container_data = {
            "test": "container_test_data",
            "test_list": [
                {
                    "test": "first_test_data",
                },
                {
                    "test": "second_test_data",
                },
            ],
            "test_model": {
                "test": "model_test_data",
            },
        }
        cls._container = _test_utils.TestContainer(
            data=cls._container_data,
        )

        cls._listing_data = [
            {
                "test": "first_test_data",
            },
            {
                "test": "second_test_data",
            },
        ]
        cls._listing = _test_utils.TestListing(
            data=cls._listing_data,
        )

        cls._values = _test_utils.TestValues(
            test="values_test_data",
        )

    def test_model(self) -> None:
        self.assert_equal(
            func_name=self.test_model.__name__,
            test_data=self._model._data,
            test_expected=self._model_data,
        )

        self.assert_equal(
            func_name=self.test_model.__name__,
            test_data=self._model.test,
            test_expected="model_test_data",
        )

    def test_container(self) -> None:
        self.assert_equal(
            func_name=self.test_container.__name__,
            test_data=self._container._data,
            test_expected=self._container_data,
        )

        self.assert_equal(
            func_name=self.test_container.__name__,
            test_data=self._container.test,
            test_expected="container_test_data",
        )

        self.assert_type(
            func_name=self.test_container.__name__,
            test_data=self._container.test_model,
            test_type=_test_utils.TestModel,
        )

        self.assert_equal(
            func_name=self.test_container.__name__,
            test_data=self._container.test_model.test,
            test_expected="model_test_data",
        )

        self.assert_type(
            func_name=self.test_container.__name__,
            test_data=self._container.test_list,
            test_type=list,
        )

        self.assert_equal(
            func_name=self.test_container.__name__,
            test_data=self._container.test_list[0].test,
            test_expected="first_test_data",
        )

        self.assert_equal(
            func_name=self.test_container.__name__,
            test_data=self._container.test_list[1].test,
            test_expected="second_test_data",
        )

    def test_listing(self) -> None:
        self.assert_equal(
            func_name=self.test_listing.__name__,
            test_data=self._listing._data,
            test_expected=self._listing_data,
        )

        self.assert_type(
            func_name=self.test_listing.__name__,
            test_data=self._listing.test_models,
            test_type=list,
        )

        self.assert_equal(
            func_name=self.test_listing.__name__,
            test_data=self._listing.test_models[0].test,
            test_expected="first_test_data",
        )

        self.assert_equal(
            func_name=self.test_listing.__name__,
            test_data=self._listing.test_models[1].test,
            test_expected="second_test_data",
        )

    def test_values(self) -> None:
        self.assert_equal(
            func_name=self.test_values.__name__,
            test_data=self._values.test,
            test_expected="values_test_data",
        )

        self._values.update(
            test="values_new_data",
        )

        self.assert_equal(
            func_name=self.test_values.__name__,
            test_data=self._values.test,
            test_expected="values_new_data",
        )
