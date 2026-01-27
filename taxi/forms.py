from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator

from taxi.models import Driver


class DriverCreationForm(UserCreationForm):

    license_number = forms.CharField(
        required=True,
        validators=[RegexValidator(r"^[A-Z]{3}\d{5}$")]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("first_name", "last_name", "license_number",))


class DriverLicenseUpdateForm(forms.ModelForm):

    license_number = forms.CharField(
        required=True,
        validators=[RegexValidator(r"^[A-Z]{3}\d{5}$")]
    )

    class Meta(UserChangeForm.Meta):
        model = Driver
        fields = ("license_number",)
