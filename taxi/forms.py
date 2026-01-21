from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.form_validators import license_number_validator
from taxi.models import Driver, Car


class LicenseNumberMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        license_number_validator(license_number)
        return license_number


class DriverCreationForm(LicenseNumberMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )


class DriverLicenseUpdateForm(LicenseNumberMixin, forms.ModelForm):
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
        fields = ("model", "manufacturer", "drivers",)
