from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "license_number",)

    def clean_license_number(self) -> str:
        license_num = self.cleaned_data["license_number"]

        if len(license_num) != 8:
            raise ValidationError("License must consist of 8 characters")
        if not license_num[:3].isupper() or not license_num[:3].isalpha():
            raise ValidationError(
                "The first three characters must be uppercase"
            )
        if not license_num[-5:].isdigit():
            raise ValidationError(
                "The last five characters must be digits"
            )

        return license_num


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return DriverForm.clean_license_number(self)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
