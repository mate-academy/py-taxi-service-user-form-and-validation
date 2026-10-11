from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_format(value):
    if len(value) == 8:
        if value[:3].isalpha() and value[:3].isupper():
            if value[3:].isdigit():
                return
    raise ValidationError(
        "Incorrect license format. "
        "Must contain 3 uppercase letters and 5 digits."
    )


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(validators=[validate_license_format])

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(validators=[validate_license_format])

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
