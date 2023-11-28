from django.core import validators
from django.utils.translation import gettext_lazy


class FirstCharactersUppercase(validators.BaseValidator):
    message = gettext_lazy(
        "First %(limit_value)s characters must be in "
        "uppercase."
    )

    def compare(self, arg1, arg2):
        return arg1 < arg2

    def clean(self, value):
        return sum(
            [
                1
                for char in value[:self.limit_value]
                if (not char.isdigit()) and char == char.upper()
            ]
        )


class LastCharactersDigits(validators.BaseValidator):
    message = gettext_lazy(
        "Last %(limit_value)s characters must be as digital."
    )

    def compare(self, arg1, arg2):
        return arg1 < arg2

    def clean(self, value):
        return sum(
            [1 for char in value[-self.limit_value:] if char.isdigit()]
        )
