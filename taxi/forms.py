from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not len(license_number) == 8:
            raise ValidationError("License number must consists of 8 symbols!")
        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError("First 3 symbols of license number must be uppercase letters!")
        if not license_number[-5:].isdigit():
            raise ValidationError("Last 5 symbols of license number must be digits!")
        return license_number


class DriverCreationForm(UserCreationForm, DriverLicenseUpdateForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "license_number")


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
