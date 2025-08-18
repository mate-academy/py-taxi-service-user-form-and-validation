from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from .models import Car

User = get_user_model()


license_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message=(
        "Value must start with 3 uppercase letters "
        "followed by 5 digits (e.g. ABC12345)."
    ),
)


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(validators=(license_validator, ))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(UserChangeForm):
    password = None
    license_number = forms.CharField(validators=(license_validator, ))

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
