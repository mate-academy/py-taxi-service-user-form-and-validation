from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from taxi.models import Driver, Car


class DriverForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if len(license_number) != 8:
            raise ValidationError(
                "License number should be 8 characters long")
        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise ValidationError(
                "First three license number should be uppercase letters"
            )
        if not license_number[3:].isdigit():
            raise ValidationError(
                "Last five license number characters should be digits only")
        return license_number


class CarForm(ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )


class Meta:
    model = Car
    fields = "__all__"
