from __future__ import annotations
import pyquoks
import _test_utils


class TestTest(pyquoks.test.TestCase):
    _MODULE_NAME = __name__

    def test_assert_is(self) -> None:
        self.assert_equal(
            func_name=self.test_assert_is.__name__,
            test_data="test_data",
            test_expected="test_data",
        )

    def test_assert_raises(self) -> None:
        self.assert_raises(
            func_name=self.test_assert_raises.__name__,
            test_func=_test_utils.raise_test_exception,
            test_exception=NotImplementedError,
        )

    def test_assert_type(self) -> None:
        self.assert_type(
            func_name=self.test_assert_type.__name__,
            test_data="test_data",
            test_type=str,
        )
