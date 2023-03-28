from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car


class DriverUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        first = license_number[:3]
        last = license_number[-5:]
        length = len(license_number)

        def contains_number(string):
            return any(char.isdigit() for char in string)

        if (length != 8
                or first.upper() != first
                or not last.isdigit()
                or contains_number(first)):
            raise ValidationError("Ensure that value is valid")

        return license_number


class CarUpdateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
