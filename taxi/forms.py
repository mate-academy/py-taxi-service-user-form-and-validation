from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxLengthValidator, MinLengthValidator

from taxi.models import Driver, Car


class LicenseNumberValidators(forms.Form):
    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        if not (license_number[:3].isupper() and license_number[:3].isalpha()):
            raise forms.ValidationError(
                "First 3 characters are uppercase letters."
            )

        if not license_number[-5:].isnumeric():
            raise forms.ValidationError(
                "Last 5 characters must be digits."
            )

        return license_number

    license_number = forms.CharField(
        required=True,
        validators=[MaxLengthValidator(8), MinLengthValidator(8)],
    )


class DriverCreatedForm(LicenseNumberValidators, UserCreationForm):

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number",
        )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class DriverLicenseUpdateForm(LicenseNumberValidators, forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreatedForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
