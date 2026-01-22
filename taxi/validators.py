from django.core.exceptions import ValidationError


class LicenseNumberValidator:
    def __call__(self, value):
        if (value[:3].isalpha() and value[:3].isupper()) and value[3:].isdigit():
            return value
        raise ValidationError("Invalid license number.")

    def deconstruct(self):
        return (f"taxi.validators.{self.__class__.__name__}",
                [],
                {})
