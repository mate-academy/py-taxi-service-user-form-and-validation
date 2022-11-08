from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[RegexValidator(regex="[A_Z]{3}[0-9]{5}",
                                   message="Invalid number",
                                   code="invalid_licence_number")])

    class Meta:
        model = Driver
        fields = ("license_number",)
