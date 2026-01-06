from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


def validate_license_number(value: str) -> str:
    value = (value or "").strip()
    if len(value) != 8:
        raise ValidationError(
            "The licence number is incorrect."
        )
    if (
            not value[:3].isalpha()
            or not value[:3].isupper()
            or not value[3:].isdigit()
    ):
        raise ValidationError(
            "The licence number is incorrect."
        )
    return value


class DriverCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        value = self.cleaned_data["license_number"]
        return validate_license_number(value)


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        value = self.cleaned_data["license_number"]
        return validate_license_number(value)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
