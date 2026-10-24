from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from .models import Car


validate_license_number = RegexValidator(
    regex=r"\A[A-Z]{3}[0-9]{5}\Z",
    message="Use 3 uppercase English letters followed by 5 digits "
            "(for example, ABC12345).",
)


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8, validators=[validate_license_number]
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8, validators=[validate_license_number]
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
