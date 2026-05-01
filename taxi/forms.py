from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def _clean_license_number(self):
    license_number = self.cleaned_data["license_number"]
    if len(license_number) == 8:
        if license_number[0:3].isalpha() and license_number[0:3].isupper():
            if license_number[3:].isnumeric():
                return license_number
    raise ValidationError("Write correct license number!")


class DriverCreateForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        return _clean_license_number(self)


class DriverLicenseUpdateForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return _clean_license_number(self)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
