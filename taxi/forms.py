from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class AuthorCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number")


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[RegexValidator(
            regex=r"[A-Z][A-Z][A-Z]\d\d\d\d\d$",
            message="license number should consist only of 8 characters. "
                    "First 3 characters are uppercase letters. "
                    "Last 5 characters are digits"
        )
        ]
    )

    class Meta:
        model = Driver
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
