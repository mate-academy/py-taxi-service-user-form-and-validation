from django import forms

from taxi.models import Driver


class DriverCreateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["username", "first_name", "last_name", "license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must" " consist of 8 characters."
            )

        if (not license_number[:3].isalpha()
                or not license_number[3:].isdigit()):
            raise forms.ValidationError(
                "Invalid format. The first 3 characters must be uppercase"
                " letters, and the last 5 characters must be digits."
            )

        return license_number


class DriverDeleteForm(forms.Form):
    confirm_delete = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        help_text="I confirm that I want to delete this driver.",
    )


class DriverUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["first_name", "last_name", "license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must consist of 8 characters."
            )

        return license_number
