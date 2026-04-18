from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car


class DriverCreationForm(UserCreationForm):
    class Meta:
        user = get_user_model()
        model = user
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if (
            license_number[:3].isupper()
            and license_number[:3].isalpha()
            and license_number[3:].isdigit()
            and len(license_number) == 8
        ):
            return license_number
        else:
            raise forms.ValidationError(
                "License number must be in the format: ABC12345"
            )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        user = get_user_model()
        model = user
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if (
            license_number[:3].isupper()
            and license_number[:3].isalpha()
            and license_number[3:].isdigit()
            and len(license_number) == 8
        ):
            return license_number
        else:
            raise forms.ValidationError(
                "License number must be in the format: ABC12345"
            )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
