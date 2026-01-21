from django.core.exceptions import ValidationError


class LicenseNumberValidationMixin:
    MIN_LENGTH = 8
    UPPER_LENGTH = 3

    def validate_license_number(self, license_number):
        if len(license_number) != LicenseNumberValidationMixin.MIN_LENGTH:
            raise (ValidationError
                   ("License number must be exactly 8 characters long."))

        if not (license_number
                [:LicenseNumberValidationMixin.UPPER_LENGTH].isupper()
                and license_number
                [:LicenseNumberValidationMixin.UPPER_LENGTH].isalpha()):
            raise (ValidationError
                   ("The first 3 characters must be uppercase letters."))

        if not license_number[3:].isdigit():
            raise (ValidationError
                   ("The last 5 characters must be digits."))

        return license_number
