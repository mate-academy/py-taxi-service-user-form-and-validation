from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    length = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_num = self.cleaned_data["license_number"]
        first_char = license_num[:3]
        last_char = license_num[3:]

        if (len(license_num) == DriverLicenseUpdateForm.length
                and first_char.isupper()
                and first_char.isalpha()
                and last_char.isnumeric()):
            return license_num

        raise ValidationError("Data is not correct")


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
