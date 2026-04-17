from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car


User = get_user_model()


class DriverCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if not license_number:
            raise forms.ValidationError("License number is required")

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License must consist of 8 characters"
            )

        if not (
            license_number[:3].isalpha()
            and license_number[:3].isupper()
            and license_number[3:].isdigit()
        ):
            raise forms.ValidationError(
                "License must be 3 uppercase letters followed by 5 digits"
            )

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if not license_number:
            raise forms.ValidationError("License number is required")

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License must consist of 8 characters"
            )

        if not (
            license_number[:3].isalpha()
            and license_number[:3].isupper()
            and license_number[3:].isdigit()
        ):
            raise forms.ValidationError(
                "License must be 3 uppercase letters followed by 5 digits"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
