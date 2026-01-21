from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from taxi.models import Car
from taxi.validators import validate_license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "license_number",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[validate_license_number],
        help_text=(
            "License number must be exactly 8 characters long. "
            "License number must start with 3 letters. "
            "License number must end with 4 digits."
        )
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number",)
