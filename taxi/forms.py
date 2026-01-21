from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Car


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError(
            "License number should consist of exactly 8 characters"
        )
    first_three_chars = license_number[:3]
    last_five_chars = license_number[-5:]
    if not (first_three_chars.isalpha() and first_three_chars.isupper()):
        raise ValidationError("Incorrect license format")
    if not last_five_chars.isdigit():
        raise ValidationError("Incorrect license format")


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(validators=[validate_license_number])

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("first_name",
                                                 "last_name",
                                                 "license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(validators=[validate_license_number])

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
