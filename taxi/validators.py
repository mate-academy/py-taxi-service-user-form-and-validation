from django.core import validators
from django.utils.translation import gettext_lazy


class FirstCharactersUppercase(validators.BaseValidator):
    message = gettext_lazy(
        "First %(limit_value)s characters must be in "
        "uppercase."
    )

    def compare(self, a, b):
        return a < b

    def clean(self, x):
        return sum(
            [1 for char in x[:self.limit_value] if char == char.upper()]
        )


class LastCharactersDigits(validators.BaseValidator):
    message = gettext_lazy(
        "Last %(limit_value)s characters must be as digital."
    )

    def compare(self, a, b):
        return a < b

    def clean(self, x):
        return sum(
            [1 for char in x[-self.limit_value:] if char.isdigit()]
        )
