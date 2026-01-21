from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}[0-9]{5}$",
                message="Ensure that your license_number has 3 first "
                        "symbols uppercase and 5 digits after!"
            )
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(f"License_number is 8 "
                                  f"symbols only! Not {len(license_number)}!")

        if (not license_number[:3].isalpha()
                or license_number[:3] != license_number[:3].upper()):
            raise ValidationError("Ensure that your license_number "
                                  "has 3 first symbols uppercase!")

        if not license_number[3:].isdigit():
            raise ValidationError("Ensure that your license "
                                  "number must have 3 uppercase "
                                  "letters followed by 5 digits!")

        return license_number
