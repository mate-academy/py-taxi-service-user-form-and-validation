from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from taxi.models import Driver, Car
from django.core.exceptions import ValidationError


class DriverLicenseUpdateForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) < 8:
            raise ValidationError("There are less than 8 characters!")
        if not license_number[:3].isupper():
            raise ValidationError(
                "First three characters should be in upper register!"
            )
        if not license_number[:3].isalpha():
            raise ValidationError("First three characters should be letters!")
        if not license_number[-5:].isdigit():
            raise ValidationError("Last five characters should be numbers!")
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
