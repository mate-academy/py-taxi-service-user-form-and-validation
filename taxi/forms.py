from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreateForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            "license_number",
        ]

    def clean_license_number(self):

        driver_license = self.cleaned_data["license_number"]

        if len(driver_license) != 8:
            raise ValidationError("License must be 8 characters long")

        for char in driver_license[:3]:
            if not char.isupper():
                raise ValidationError("First three chars must "
                                      "be an uppercase letter")

        for char in driver_license[-5:]:
            if not char.isnumeric():
                raise ValidationError("Last five chars must be a digit")
        return driver_license


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
