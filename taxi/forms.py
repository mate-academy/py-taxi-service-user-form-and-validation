from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car
from taxi.validators import validate_license_number


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class DriverAssignForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
