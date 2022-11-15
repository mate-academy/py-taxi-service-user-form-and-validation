from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenseValidateMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not len(license_number) == 8:
            raise ValidationError("length is not equal to 8")

        if not (license_number[0:3].isalpha()
                and license_number[0:3].isupper()):
            raise ValidationError(
                "the first 3 symbols are not uppercase letters"
            )

        if not license_number[3:].isnumeric():
            raise ValidationError("the last 5 characters are not numbers")

        return license_number


class DriverLicenseUpdateForm(LicenseValidateMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreationForm(LicenseValidateMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
