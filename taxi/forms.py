from django.core.exceptions import ValidationError

from django.contrib.auth.forms import UserCreationForm
from taxi.models import Driver


class DriverLicenseUpdateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    # def clean_license_number(self):
    #     license_number = self.cleaned_data["license_number"]
    #     if (
    #             len(license_number) != 8 or
    #             license_number[:4] != "".join(license_number[:4]).lower() or not
    #             "".join(license_number[3:]).isdigit()
    #     ):
    #         raise ValidationError("Input correct data as 'AAA12345'")
