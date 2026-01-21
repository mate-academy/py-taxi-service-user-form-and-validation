from django.core.exceptions import ValidationError


class LicenseNumberValidationMixin:

    def clean_license_number(self):
        if hasattr(self, "cleaned_data"):
            license_num = self.cleaned_data.get("license_number")
            if not license_num[:3].isupper() or not license_num[:3].isalpha():
                raise ValidationError(
                    "First 3 characters must be uppercase letters."
                )

            if not license_num[3:].isdigit():
                raise ValidationError("Last 5 characters must be digits.")

            return license_num
