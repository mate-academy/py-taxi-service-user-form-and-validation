from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CleanLicenseMixin:
    def clean_license_number(self):
        license_num = self.cleaned_data["license_number"]
        if len(license_num) != 8:
            raise ValidationError(
                "License number should consist only of 8 characters!"
            )
        if not license_num[:3].isalpha() or not license_num[:3].isupper():
            raise ValidationError(
                "License number first 3 characters should be "
                "as upper case letters!"
            )
        if not license_num[3:].isdigit():
            raise ValidationError(
                "License number last 5 character should be digits!"
            )
        return license_num


class DriverLicenseUpdateForm(CleanLicenseMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )


class DriverCreationForm(CleanLicenseMixin, UserCreationForm):
    class Meta(UserCreationForm):
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number")


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
