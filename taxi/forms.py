from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreateForm(UserCreationForm):

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License number must be 8 symbols")

        if not license_number[:3].isalpha():
            raise ValidationError("First three symbols must be alpha symbols")
        elif not license_number[:3].isupper():
            raise ValidationError("First three symbols must be in uppercase")
        if not license_number[3:].isdigit():
            raise ValidationError("Last symbols must be digit")

        return license_number

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(max_length=8)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License number must be 8 symbols")

        if not license_number[:3].isalpha():
            raise ValidationError("First three symbols must be alpha symbols")
        elif not license_number[:3].isupper():
            raise ValidationError("First three symbols must be in uppercase")
        if not license_number[3:].isdigit():
            raise ValidationError("Last symbols must be digit")

        return license_number

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
