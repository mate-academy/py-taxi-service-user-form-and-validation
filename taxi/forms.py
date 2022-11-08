from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Driver


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[RegexValidator(regex="[A-Z]{3}\\d{5}$",
                                   message="Invalid number",
                                   code="invalid_licence_number")])

    class Meta:
        model = Driver
        fields = ("license_number",)
