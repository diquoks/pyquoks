from __future__ import annotations
import pyquoks.test


class TestTest(pyquoks.test.TestBase):
    def test_assert_is(self) -> None:
        func_name = self.test_assert_is.__name__
        test_data = "test_data"
        test_expected = "test_data"

        self.assert_is(
            func_name,
            test_data,
            test_expected,
        )

    def test_assert_type(self) -> None:
        func_name = self.test_assert_type.__name__
        test_data = "test_data"
        test_type = str

        self.assert_type(
            func_name,
            test_data,
            test_type,
        )
