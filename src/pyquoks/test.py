from __future__ import annotations
import unittest, types
import pyquoks.data


class TestBase(unittest.TestCase):
    """
    Class for performing unit testing
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls._logger = pyquoks.data.LoggerService(
            name=__name__,
        )

    def assert_is(
            self,
            func_name: str,
            test_data: object,
            test_expected: object,
    ):
        self._logger.info(
            msg=(
                f"{func_name}:\n"
                f"Data: {test_data}\n"
                f"Expected: {test_expected}\n"
            ),
        )

        try:
            self.assertIs(
                expr1=test_data,
                expr2=test_expected,
            )
        except Exception as e:
            self._logger.log_error(e)

    def assert_type(
            self,
            func_name: str,
            test_data: object,
            test_type: type | types.UnionType,
    ) -> None:
        self._logger.info(
            msg=(
                f"{func_name}:\n"
                f"Type: {type(test_data).__name__}\n"
                f"Expected: {test_type.__name__}\n"
            ),
        )

        # TODO: log attributes of pyquoks' classes

        try:
            self.assertIsInstance(
                obj=test_data,
                cls=test_type,
            )
        except Exception as e:
            self._logger.log_error(e)
