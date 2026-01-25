from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class LicenseNumberValidator:
    LICENSE_NUM_LEN = 8

    def __call__(self, value: str) -> None:
        if len(value) != self.LICENSE_NUM_LEN:
            raise ValidationError(
                "License number must "
                "contain 8 characters"
            )
        first_vals = value[:3]
        if not (
            first_vals.isascii()
            and first_vals.isalpha()
            and first_vals.isupper()
        ):
            raise ValidationError(
                "First three values of license "
                "number must be uppercase letters"
            )
        if not value[-5:].isdigit():
            raise ValidationError(
                "Last five values of license "
                "number must be digits"
            )

    def __eq__(self, other) -> bool:
        return isinstance(
            other,
            LicenseNumberValidator
        )
