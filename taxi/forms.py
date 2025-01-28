from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from taxi.models import Driver, Car


license_length = 8


def validate_license_number(value):
    if len(value) != license_length:
        raise ValidationError(f"Must be {license_length} characters long")
    if not value[:3].isupper() or not value[:3].isalpha():
        raise ValidationError("First 3 symbols should be alphabetic")
    if not value[3:].isdigit():
        raise ValidationError("Last 5 symbols should be digit.")


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields


class DriverLicenseUpdateForm(forms.ModelForm):
    license_length = 8

    license_number = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(license_length),
            MaxLengthValidator(license_length),
            validate_license_number]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
