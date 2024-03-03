from django import forms

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("first_name", "last_name", "license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if (not license_number[:3].isupper()
                or not license_number[:3].isalpha()):
            raise forms.ValidationError(
                "First 3 characters must be letters in uppercase"
            )
        elif not license_number[3:].isdigit():
            raise forms.ValidationError(
                "Last 5 characters must be digits"
            )
        elif len(license_number) != 8:
            raise forms.ValidationError(
                "Length of license number must be 8"
            )
        return license_number


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
