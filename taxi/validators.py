from django.forms import ValidationError
from django.core.validators import RegexValidator


class LicenseValidator(RegexValidator):
    def __init__(self, message=None, code=None):
        super().__init__(regex=None, message=message, code=code)

    def __call__(self, value: str) -> None:
        if not (
            len(value) == 8
            and value[:3].isalpha()
            and value[:3].isascii()
            and value[3:].isdigit()
            and value[:3] == value[:3].upper()
        ):
            raise ValidationError(
                "Licence number must contain 3 uppercase letters and 5 numbers"
            )
