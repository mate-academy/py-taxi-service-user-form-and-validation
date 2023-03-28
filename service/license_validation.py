from django.core.exceptions import ValidationError


def license_validation(self):
    license_number = self.cleaned_data["license_number"]
    if not (
            len(license_number) == 8
            and license_number[:3].isalpha()
            and license_number[:3].isupper()
            and license_number[-5::].isdigit()
    ):
        raise ValidationError("Incorrect data")

    return license_number
