from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Driver, Car


class CleanLicenseNumberMixin:
    def clean_license_number(self):
        license_n = self.cleaned_data["license_number"]
        if not (license_n[:3].isalpha() and license_n[:3].isupper()):
            raise ValidationError(
                "The first three characters must be upper case letters!"
            )
        if not len(license_n) == 8:
            raise ValidationError(
                "The license number must contain 8 characters!"
            )
        if not license_n[3:].isdecimal():
            raise ValidationError(
                "The license number must contain 5 decimals!"
            )
        return license_n


class DriverCreationForm(CleanLicenseNumberMixin, UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(CleanLicenseNumberMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        required=True,
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"


class CarUpdateDriverForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = []
