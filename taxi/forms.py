from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


from taxi.models import Car

User = get_user_model()


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be exactly 8 characters.")

        if (not license_number[:3].isupper()
                or not license_number[:3].isalpha()):
            raise forms.ValidationError(
                "First 3 characters must be uppercase letters.")

        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "Last 5 characters must be digits.")

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be exactly 8 characters.")

        if (not license_number[:3].isupper()
                or not license_number[:3].isalpha()):
            raise forms.ValidationError(
                "First 3 characters must be uppercase letters.")

        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "Last 5 characters must be digits.")

        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")  # include drivers field
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),  # <-- use checkboxes
        }
