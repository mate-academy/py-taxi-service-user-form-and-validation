from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Car


license_format = forms.CharField(validators=[RegexValidator(
    regex=r"^[A-Z]{3}[0-9]{5}$",
    message=(
        "License must be exactly 8 characters:"
        " 3 uppercase letters followed by 5 digits.\n"
        "Example: ABC12345"
    ),
    code="invalid_license_format"
)])


class DriverUserCreationForm(UserCreationForm):
    license_number = license_format

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = license_format

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
