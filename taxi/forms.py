from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Car
from taxi.validators import LicenseNumberValidator


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[LicenseNumberValidator()],
        max_length=8,
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            UserCreationForm.Meta.fields + (
                "first_name",
                "last_name",
                "license_number",
            )
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[LicenseNumberValidator()],
        max_length=8,
    )

    class Meta:
        model = get_user_model()
        fields = (
            "license_number",
        )


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
