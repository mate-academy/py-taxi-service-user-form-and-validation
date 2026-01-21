from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator, MaxLengthValidator

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    MIN_LICENSE_NUMBER = 8

    license_number = forms.CharField(
        validators=[MaxLengthValidator(MIN_LICENSE_NUMBER),
                    RegexValidator(regex=r"^[A-Z]{3}\d{5}$")]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    MIN_LICENSE_NUMBER = 8

    license_number = forms.CharField(
        validators=[MaxLengthValidator(MIN_LICENSE_NUMBER),
                    RegexValidator(regex=r"^[A-Z]{3}\d{5}$")]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
