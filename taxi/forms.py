from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenceValidateMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"] # noqa

        if not (
                len(license_number) == 8
                and license_number[0:2].isupper()
                and license_number[0:2].isalpha()
                and license_number[3:].isnumeric()
        ):
            raise ValidationError(
                "The driver's license must be in the format 'XXX00000' "
                "(3 uppercase letters and 5 numbers)"
            )

        return license_number


class DriverLicenseUpdateForm(LicenceValidateMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreationForm(LicenceValidateMixin, UserCreationForm):
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
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
