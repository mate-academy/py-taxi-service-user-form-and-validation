from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Car

User = get_user_model()

code_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="Must be 8 chars: first 3 uppercase "
            "letters (A-Z), then 5 digits (0-9)."
)


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[code_validator],
        widget=forms.TextInput(attrs={"placeholder": "Enter license number"})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (UserCreationForm.Meta.fields
                  + ("username", "first_name", "last_name",
                     "email", "license_number"))


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[code_validator],
        widget=forms.TextInput(attrs={"placeholder": "Enter license number"})
    )

    class Meta:
        model = User
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
