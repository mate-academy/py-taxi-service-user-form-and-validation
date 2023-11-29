from django.core.exceptions import ValidationError
from django import forms


class LicenseNumberValidationMixin(forms.ModelForm):
    LENGTH = 8
    FIRST_PART_LENGTH = 3
    LAST_PART_LENGTH = 5

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LENGTH:
            raise ValidationError(
                f"The length of licence number must be equal to {self.LENGTH}."
            )
        if (
                not license_number[:self.FIRST_PART_LENGTH].isalpha()
                or not license_number[:self.FIRST_PART_LENGTH].isupper()
        ):
            raise ValidationError(
                f"First {self.FIRST_PART_LENGTH} "
                "characters must be uppercase letters."
            )
        if not license_number[-self.LAST_PART_LENGTH:].isdigit():
            raise ValidationError(
                f"Last {self.LAST_PART_LENGTH} characters must be digits."
            )

        return license_number
