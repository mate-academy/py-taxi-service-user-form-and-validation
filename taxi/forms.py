from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from taxi.models import Car


license_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="License number must contain 3 uppercase letter and 5 digits."
)


class DriverForm(UserCreationForm):

    license_number = forms.CharField(validators=[license_validator])

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):

    license_number = forms.CharField(validators=[license_validator])

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
