from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(value):
    if len(value) != 8:
        raise ValidationError("Ensure that value is 8 characters.")
    if not all("A" <= c <= "Z" for c in value[:3]):
        raise ValidationError("First 3 characters must be uppercase letters.")
    if not value[3:].isdigit():
        raise ValidationError("Last 5 characters must only contain numbers.")


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=255, required=True, validators=[validate_license_number]
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=255, required=True, validators=[validate_license_number]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
