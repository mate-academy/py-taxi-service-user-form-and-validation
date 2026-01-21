from abc import abstractmethod
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Driver, Car
from django.contrib.auth.forms import UserCreationForm


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    @abstractmethod
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("license number len must be 8 characters")
        elif license_number[0:4] != license_number[0:4].upper():
            raise ValidationError("first 3 symbols must be in upper case")
        elif license_number[0].isdigit():
            raise ValidationError("first symbol is int")
        elif license_number[1].isdigit():
            raise ValidationError("second symbol is int")
        elif license_number[2].isdigit():
            raise ValidationError("third symbol is int")
        elif not license_number[3:].isdigit():
            raise ValidationError("last 5 symbol must be int")

        return license_number


class DriverCreateForm(UserCreationForm, DriverLicenseUpdateForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "license_number"
        )

    def clean_license_number(self):
        return super().clean_license_number()


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
