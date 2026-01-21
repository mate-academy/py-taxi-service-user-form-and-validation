from django.core.exceptions import ValidationError


class DriverValidationLicenseNumber:
    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        condition_ = (len(license_number) == 8
                      and license_number[:3].isupper()
                      and license_number[:3].isalpha()
                      and license_number[3:].isnumeric())
        if not condition_:
            raise ValidationError("License number invalid")

        return license_number
