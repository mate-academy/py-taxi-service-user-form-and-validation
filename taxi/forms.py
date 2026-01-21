from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class BaseDriverForm(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        letters, digits = license_number[:3], license_number[3:]
        if (
                len(license_number) == 8
                and letters.isalpha()
                and letters.isupper()
                and digits.isdigit()
        ):
            return license_number
        raise ValidationError(
            "License number must have 3 "
            "uppercase letters followed by 5 digits."
        )


class DriverCreationForm(UserCreationForm, BaseDriverForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (
            UserCreationForm.Meta.fields
            + ("license_number", "first_name", "last_name",)
        )


class DriverLicenseUpdateForm(BaseDriverForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
