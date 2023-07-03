from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    MAX_LEN = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_data = self.cleaned_data["license_number"]
        if len(license_data) != DriverLicenseUpdateForm.MAX_LEN:
            raise ValidationError(
                f"Number of characters"
                f" must be {DriverLicenseUpdateForm.MAX_LEN}"
            )
        second_part = license_data[3:]
        first_part = license_data[:3]
        if not first_part.isalpha() or not first_part.isupper():
            raise ValidationError("First characters must be capital letters")
        if not second_part.isdecimal():
            raise ValidationError("Last 5 characters must be digits")
        return license_data


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
