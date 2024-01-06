from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxLengthValidator, MinLengthValidator

from taxi.models import Driver, Car


class LicenseNumberValidationMixin(forms.Form):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if (
            not license_number[:3].isupper()
            or not license_number[:3].isalpha()
        ):
            raise forms.ValidationError(
                "The first three characters must be uppercase letters."
            )

        if not license_number[-5:].isnumeric():
            raise forms.ValidationError("Last 5 characters must be digits.")

        return license_number


class DriverCreationForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    license_number = forms.CharField(
        required=True,
        validators=[MaxLengthValidator(8), MinLengthValidator(8)],
    )


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    license_number = forms.CharField(
        required=True,
        validators=[MaxLengthValidator(8), MinLengthValidator(8)],
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Car
        fields = "__all__"
