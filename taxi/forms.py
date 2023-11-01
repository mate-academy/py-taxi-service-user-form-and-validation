from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number", )

    def clean_license_number(self):
        TRUE_LICENSE_NUMBER = 8
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != TRUE_LICENSE_NUMBER:
            raise ValidationError("entered value is not ", TRUE_LICENSE_NUMBER)
        if not (
                license_number[:3].isupper()
                or not license_number[:3].isalpha()
        ):
            raise ValidationError(
                "first three elements of license "
                "number must be upper and consist only letter"
            )
        if not license_number[-5:].isdigit():
            raise ValidationError(
                "last five elements of  must be upper and consist only digits"
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
