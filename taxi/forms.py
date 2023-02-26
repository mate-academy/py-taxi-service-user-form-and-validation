from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[RegexValidator(
            regex="^[A-Z]{3}[0-9]{5}$",
            message="License number must consist of 8 characters: "
            "3 uppercase letters and 5 digits."
        )]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number"
        )


class DriverLicenseUpdateForm(UserChangeForm):
    password = None
    license_number = forms.CharField(
        required=True,
        validators=[RegexValidator(
            regex="^[A-Z]{3}[0-9]{5}$",
            message="License number must consist of 8 characters: "
            "3 uppercase letters and 5 digits."
        )]
    )

    class Meta(UserChangeForm.Meta):
        model = Driver
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
