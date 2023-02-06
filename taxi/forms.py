from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        if len(self.cleaned_data["license_number"]) != 8:
            raise ValidationError(
                "License number should consist of 8 characters"
            )
        elif not self.cleaned_data["license_number"][:3].isupper() \
                or not self.cleaned_data["license_number"][:3].isalpha():
            raise ValidationError(
                "First 3 characters should be uppercase letters"
            )
        elif not self.cleaned_data["license_number"][3:].isdigit():
            raise ValidationError("Last 5 characters should be digits")

        return self.cleaned_data["license_number"]


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
