from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


license_number_regex = RegexValidator(regex=r"^[A-Z]{3}\d{5}$")
license_number_field = forms.CharField(
    required=True,
    max_length=8,
    min_length=3,
    validators=[license_number_regex],
    help_text="<ul>"
              "  <li>Consist only of 8 characters</li>"
              "  <li>First 3 characters are uppercase letters</li>"
              "  <li>Last 5 characters are digits</li>"
              "</ul>",
)


class DriverCreateForm(UserCreationForm):
    license_number = license_number_field

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = license_number_field

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers",)
