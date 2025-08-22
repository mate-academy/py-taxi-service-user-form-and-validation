from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Car


def validate_license_number(value):
    chars_in_license = 8
    uppercase_letters = 3
    digits = 5

    if (
            len(value) == chars_in_license
            and value[:uppercase_letters].isupper()
            and value[:uppercase_letters].isalpha()
            and value[-digits:].isnumeric()
    ):
        return value
    raise ValidationError(
        f"Ensure that value is == {chars_in_license}, "
        f"first {uppercase_letters} characters are upper, "
        f"last {digits} characters are digits"
    )


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[validate_license_number]
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number", )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[validate_license_number]
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
