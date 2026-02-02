import pyquoks


class StringsProvider(pyquoks.providers.strings.StringsProvider):
    test: TestStrings


class TestStrings(pyquoks.providers.strings.Strings):
    @property
    def test_string(self) -> str:
        return "strings_provider_test_data"
