from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if (
                len(license_number) == 8
                and license_number[:3].isupper()
                and license_number[:3].isalpha()
                and license_number[-5:].isdigit()
        ):
            return license_number
        else:
            raise ValidationError(
                "License number should consist of 8 characters\n"
                "First 3 characters should be uppercase letters\n"
                "Last 5 characters should be digits"
            )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if (
            len(license_number) == 8
            and license_number[:3].isupper()
            and license_number[:3].isalpha()
            and license_number[-5:].isdigit()
        ):
            return license_number
        else:
            raise ValidationError(
                "License number should consist of 8 characters\n"
                "First 3 characters should be uppercase letters\n"
                "Last 5 characters should be digits"
            )


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
