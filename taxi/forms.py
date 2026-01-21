from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


LICENSE_PATTERN = r"^[A-Z]{3}[0-9]{5}$"

license_number = forms.CharField(
    validators=[RegexValidator(
        regex=LICENSE_PATTERN,
        message="License number must follow the format: XXX12345.",
    )]
)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreateForm(UserCreationForm):
    cars = forms.ModelMultipleChoiceField(
        queryset=Car.objects,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    license_number = license_number

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", "cars")


class DriverLicenseUpdateForm(forms.ModelForm):

    license_number = license_number

    class Meta:
        model = Driver
        fields = ("license_number",)
