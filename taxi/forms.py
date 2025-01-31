from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from taxi.models import Driver, Car


LICENSE_MAX_LENGTH = 8
LICENSE_PREFIX_LENGTH = 3
LICENSE_SUFFIX_LENGTH = 3


def validate_license_number(license_number):
    if len(license_number) != LICENSE_MAX_LENGTH:
        raise ValidationError("Must be 8 characters long")
    if (not license_number[:LICENSE_PREFIX_LENGTH].isupper()
            or not license_number[:LICENSE_PREFIX_LENGTH].isalpha()):
        raise ValidationError("First 3 symbols should be alphabetic")
    if not license_number[LICENSE_SUFFIX_LENGTH:].isdigit():
        raise ValidationError("Last 5 symbols should be digit.")


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clear_license_number(self) -> str:
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    license_length = 8

    license_number = forms.CharField(
        required=True,
        validators=[validate_license_number]
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
