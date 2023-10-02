from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import Driver, Car


def licence_is_valid(lic_num):
    if len(lic_num) != 8:
        raise ValidationError(
            "License number should be exactly 8 characters long"
        )
    elif lic_num[:3] != lic_num[:3].upper() or not lic_num[:3].isalpha():
        raise ValidationError("First 3 letters should be uppercase")
    elif not lic_num[-5:].isdigit():
        raise ValidationError("Last 5 symbols should be digits")


class LicenseNumberValidationMixin(forms.Form):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        licence_is_valid(license_number)
        return license_number


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Driver
        fields = ("license_number", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()


class BookForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
