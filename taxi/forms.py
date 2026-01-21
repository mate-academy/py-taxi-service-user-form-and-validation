from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator

from taxi.mixins import LicenseNumberValidationMixin
from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm, LicenseNumberValidationMixin):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers",)


class DriverLicenseUpdateForm(forms.ModelForm, LicenseNumberValidationMixin):
    license_number = forms.CharField(
        required=True,
        validators=[MaxLengthValidator(8), MinLengthValidator(8)]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)
