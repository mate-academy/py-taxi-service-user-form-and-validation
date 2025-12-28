from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Driver
        fields = ("license_number", )


    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise ValidationError("License number must be 8 digits")
        elif not license_number[:3].isupper() and license_number[:3].isalpha():
            raise ValidationError("First 3 symbols must be uppercase")
        elif not license_number[-5:].isdigit():
            raise ValidationError("Last 5 symbols must be digits")
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
