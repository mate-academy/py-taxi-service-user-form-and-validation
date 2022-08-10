from django.contrib.auth.forms import UserCreationForm
from django import forms


from taxi.models import Driver
from taxi.validation import LicenseValidationMixin


class DriverCreationForm(LicenseValidationMixin, UserCreationForm):
    license_number = forms.CharField(
        required=False,
        help_text="<li>License number must contain exactly 8 characters</li>"
                  "<li>First 3 characters are uppercase letters</li>"
                  "<li>Last 5 characters are digits</li>",
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseValidationMixin, forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)
