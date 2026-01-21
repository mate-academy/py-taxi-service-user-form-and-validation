from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Car


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(max_length=8)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )

    def clean_license_number(self):
        data = self.cleaned_data["license_number"]
        if (not data[:3].isalpha() or not data[:3].isupper()
                or not data[3:].isdigit() or len(data) != 8):
            raise ValidationError(
                "License number must start with"
                " 3 uppercase letters and end with 5 digits"
            )
        return data


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)
        widgets = {
            "license_number": forms.TextInput(
                attrs={
                    "placeholder": "XXX00000",
                    "maxlength": "8",
                })
        }

    def clean_license_number(self):
        data = self.cleaned_data["license_number"]
        if (not data[:3].isalpha() or not data[:3].isupper()
                or not data[3:].isdigit() or len(data) != 8):
            raise ValidationError(
                "License number must start with"
                " 3 uppercase letters and end with 5 digits."
            )

        return data


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("drivers",)
