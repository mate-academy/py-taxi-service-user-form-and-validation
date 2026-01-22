from django import forms
from .models import Driver, Car


from django import forms
from .models import Driver

class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError("License number must be exactly 8 characters long.")

        first_part = license_number[:3]
        second_part = license_number[3:]

        if not (first_part.isalpha() and first_part.isupper()):
            raise forms.ValidationError("The first 3 characters must be uppercase letters.")

        if not second_part.isdigit():
            raise forms.ValidationError("The last 5 characters must be digits.")

        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError("License number must be exactly 8 characters long.")

        first_part = license_number[:3]
        second_part = license_number[3:]

        if not (first_part.isalpha() and first_part.isupper()):
            raise forms.ValidationError("The first 3 characters must be uppercase letters.")

        if not second_part.isdigit():
            raise forms.ValidationError("The last 5 characters must be digits.")

        return license_number

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
        widgets = {
            "drivers": forms.CheckboxSelectMultiple()
        }
