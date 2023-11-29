from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car
from validations.license_validation import LicenseNumberValidationMixin


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number", )


class CarCreationForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ("model", "manufacturer",)


class CarUpdateForm(CarCreationForm):
    fields = ("drivers",)
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
