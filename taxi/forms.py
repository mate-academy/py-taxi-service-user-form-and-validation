from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from .models import Driver, Car


def validate_license_number(license_number: str):
    if len(license_number) == 8:
        for i in range(len(license_number)):
            if i <= 2 and not license_number[i].isupper():
                raise ValidationError(
                    "First three characters "
                    "of license number must be in uppercase"
                )
            if i > 2 and not license_number[i].isdigit():
                raise ValidationError(
                    "Last five characters of license number must be integers"
                )
    else:
        raise ValidationError(
            "Length of license number must be equal 8"
        )
    return license_number


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=255,
        validators=[validate_license_number],
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=255,
        validators=[validate_license_number],
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
