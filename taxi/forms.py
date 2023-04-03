from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car


class DriverUpdateForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        first_license_character = license_number[:3]
        last_license_character = license_number[-5:]
        length = len(license_number)

        def contains_number(string):
            if string.isalpha():
                return False
            return True

        if (length != 8
                or not first_license_character.isupper()
                or not last_license_character.isdigit()
                or contains_number(first_license_character)):
            raise ValidationError("Make sure that you've entered correct values")

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
