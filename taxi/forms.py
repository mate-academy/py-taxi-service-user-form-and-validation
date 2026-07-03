from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


def validate_license_number(value):
    if len(value) != 8:
        raise ValidationError("License must be exactly 8 characters")

    if not value[:3].isupper() or not value[:3].isalpha():
        raise ValidationError("First 3 characters must be uppercase letters")

    if not value[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits")

    return value


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(validators=[validate_license_number])

    class Meta:
        model = get_user_model()
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(max_length=8)

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])

    class Meta:
        model = get_user_model()
        fields = "__all__"
