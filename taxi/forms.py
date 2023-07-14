from django import forms
from django.contrib.auth.forms import UserCreationForm
from taxi.models import Car, Driver
from django.forms import ModelForm, ValidationError
from django.contrib.auth import get_user_model


class DriverCreationForm(UserCreationForm):

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )

    def clean_license_number(self) -> str:
        data = self.cleaned_data["license_number"]
        if not len(data) == 8:
            raise ValidationError(
                "Driver license number should consists of 8 characters"
            )
        if not data[0:3].isupper():
            raise ValidationError(
                "First 3 characters should be uppercase letters"
            )
        if not data[3:].isdigit():
            raise ValidationError("Last 5 characters should be digits")
        return data


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self) -> str:
        data = self.cleaned_data["license_number"]
        if not len(data) == 8:
            raise ValidationError(
                "Driver license number should consists of 8 characters"
            )
        if not data[0:3].isupper():
            raise ValidationError(
                "First 3 characters should be uppercase letters"
            )
        if not data[3:].isdigit():
            raise ValidationError("Last 5 characters should be digits")
        return data


class CarForm(ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
