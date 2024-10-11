from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Car
from .validators import LICENSE_NUMBER_VALIDATION


class DriverCreationForm(UserCreationForm):
    license_number = LICENSE_NUMBER_VALIDATION

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = LICENSE_NUMBER_VALIDATION

    class Meta:
        model = get_user_model()
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
