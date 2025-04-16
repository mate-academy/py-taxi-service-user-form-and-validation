from django import forms
from .models import Driver, Car
from django.contrib.auth.forms import UserCreationForm


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple()
        }


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError("The license number "
                                        "must be 8 characters long.")

        part_one = license_number[:3]
        part_two = license_number[3:]

        if not part_one.isalpha() or not part_one.isupper():
            raise forms.ValidationError("The first three characters"
                                        " must be capital letters.")

        if not part_two.isdigit():
            raise forms.ValidationError("The last 5 characters"
                                        " must be numbers")

        return license_number
