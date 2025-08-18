import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from taxi.models import Driver, Car

User = get_user_model()

licence_regex = RegexValidator(
    regex=re.compile(r"^[A-Z]{3}\d{5}$"),
    message="Please open your eyes and see how it must be: ABC12345",
)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        min_length=8,
        max_length=8,
        help_text="Format: ABC12345",
        validators=(licence_regex,)
    )

    class Meta:
        model = User
        fields = ["license_number"]

    def clean_license_number(self):
        value = self.cleaned_data["license_number"].strip().upper()
        return value


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        min_length=8,
        max_length=8,
        help_text="Format: ABC12345",
        strip=True,
        validators=(licence_regex,)
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number"
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
