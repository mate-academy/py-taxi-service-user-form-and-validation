from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("Length was expected to be 8")

        if not all(65 <= ord(char) <= 90 for char in license_number[:3]):
            raise ValidationError("The first three characters were"
                                  " expected to be uppercase letters")

        if not license_number[3:].isdigit():
            raise ValidationError("The last five characters were"
                                  " expected to be digits")

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("Length was expected to be 8")

        if not all(65 <= ord(char) <= 90 for char in license_number[:3]):
            raise ValidationError("The first three characters were"
                                  " expected to be uppercase letters")

        if not license_number[3:].isdigit():
            raise ValidationError("The last five characters were"
                                  " expected to be digits")

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
