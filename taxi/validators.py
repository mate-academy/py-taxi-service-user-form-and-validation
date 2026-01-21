from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class LicenseValidator:
    def __call__(self, value):
        if len(value) != 8:
            raise ValidationError("License number must be 8 characters long")
        if not value[:3].isupper() or not value[:3].isalpha():
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )
        if not value[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits")
