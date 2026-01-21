from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car
from .constants import LICENSE_RE, LICENSE_MESSAGE

User = get_user_model()

LICENSE_PATTERN = r"^[A-Z]{3}\d{5}$"


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
            "email",
        )

    def clean_license_number(self):
        value = (self.cleaned_data.get("license_number") or "").strip().upper()
        if not LICENSE_RE.fullmatch(value):
            raise ValidationError(LICENSE_MESSAGE)
        return value


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["license_number"]

    def clean_license_number(self):
        value = (self.cleaned_data.get("license_number") or "").strip().upper()
        if not LICENSE_RE.fullmatch(value):
            raise ValidationError(LICENSE_MESSAGE)
        return value
