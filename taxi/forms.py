from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("license len should be equal to 8")
        print([64 < ord(char) < 91 for char in license_number[:3]])
        if not all(64 < ord(char) < 91 for char in license_number[:3]):
            raise ValidationError(
                "first 3 license character should be uppercase letters"
            )
        if not license_number[-5:].isnumeric():
            raise ValidationError("last 5 license character should be numbers")
        return license_number


class DriverCreationForm(UserCreationForm, DriverLicenseUpdateForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
