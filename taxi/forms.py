from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car

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
        value = self.cleaned_data.get("license_number", "")
        import re
        if not re.fullmatch(LICENSE_PATTERN, value):
            raise ValidationError(
                "License must be 8 chars: 3 uppercase "
                "letters + 5 digits (e.g. ABC12345)."
            )
        return value


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["license_number"]

    def clean_license_number(self):
        value = self.cleaned_data.get("license_number", "")
        import re
        if not re.fullmatch(LICENSE_PATTERN, value):
            raise ValidationError(
                "License must be 8 chars: 3 uppercase"
                " letters + 5 digits (e.g. ABC12345)."
            )
        return value
