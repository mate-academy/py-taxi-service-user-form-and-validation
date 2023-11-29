from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError

from re import compile, fullmatch


from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_PATTERN = compile(r"^[A-Z][A-Z][A-Z]\d\d\d\d\d$")

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        if not fullmatch(self.LICENSE_PATTERN, license_number):
            raise ValidationError(
                "The license number is incorrect! "
                "Options: "
                "The length should be only 8 characters. "
                "The first 3 characters must be capitalized letters. "
                "The last 5 characters must be numbers."
            )
        return license_number


class DriverCreateForm(UserCreationForm, DriverLicenseUpdateForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class CarDriverForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ("drivers",)
