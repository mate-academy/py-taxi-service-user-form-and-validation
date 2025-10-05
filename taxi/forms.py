from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django import forms

from taxi.models import Car


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        min_length=8,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}[0-9]{5}$",
            )
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):

    license_number = forms.CharField(
        max_length=8,
        min_length=8,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}[0-9]{5}$",
            )
        ]
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers",)
