import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from .models import Driver, Car


def validate_license_number(license_number):
    if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
        raise ValidationError("License must be 3 uppercase letters + 5 digits")


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(validators=[validate_license_number])

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",
                                                 "first_name",
                                                 "last_name")


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(validators=[validate_license_number])

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["drivers"].widget = forms.CheckboxSelectMultiple()
        self.fields["drivers"].queryset = get_user_model().objects.all()

    class Meta:
        model = Car
        fields = "__all__"
