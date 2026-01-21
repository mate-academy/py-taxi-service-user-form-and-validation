from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


license_number = forms.CharField(
    max_length=8,
    validators=[
        RegexValidator(
            regex=r"^[A-Z]{3}\d{5}$",
            message="License number must consist of 3"
                    " uppercase letters followed by 5 digits."
        )
    ],
    widget=forms.TextInput(
        attrs={"placeholder": "Enter your license number"}
    ),
    required=True,
    label="License Number",
    help_text="Format: 3 uppercase letters followed by 5 digits.",
)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = license_number

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)


class DriverCreateForm(UserCreationForm):
    license_number = license_number

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "email", "license_number"
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
