from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Car
from .validators import validate_license_number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        required=False,
        validators=[validate_license_number],
        help_text="Must match the following pattern: ABC12345",
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "license_number", )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[validate_license_number],
        help_text="Must match the following pattern: ABC12345",
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number", )
