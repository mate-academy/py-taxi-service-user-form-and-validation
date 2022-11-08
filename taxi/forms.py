from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from .models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "email", "first_name", "last_name",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_SYMBOL_LEN = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LICENSE_SYMBOL_LEN:
            raise ValidationError(
                f"Your license must consist of "
                f"{self.LICENSE_SYMBOL_LEN} symbols"
            )

        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError(
                "First 3 symbols of your license must consist of "
                "letters in uppercase"
            )

        if not license_number[-5:].isdigit():
            raise ValidationError(
                "Last 5 symbols of your license must consist of digits"
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
