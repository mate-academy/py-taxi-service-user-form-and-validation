from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (UserCreationForm.Meta.fields
                  + ("license_number", "first_name", "last_name",))

    def clean_license_number(self):
        return license_number_validator(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        return license_number_validator(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


def license_number_validator(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError("License number should be 8 chars long")
    elif not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError("First 3 chars should be upper letters")
    elif not license_number[3:].isdigit():
        raise ValidationError("Last 5 chars should be digits")

    return license_number
