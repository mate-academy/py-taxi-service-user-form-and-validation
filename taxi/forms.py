from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Car, Driver
from taxi.validators import license_number_validator


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        help_text="<ul><li>Consist only of 8 characters</li> "
                  "<li>First 3 characters are uppercase letters</li>"
                  "<li>Last 5 characters are digits</li></ul>"
    )

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        data = self.cleaned_data["license_number"]
        license_number_validator(data)
        return data


class DriverForm(DriverLicenseUpdateForm, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class CarCreateForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=get_user_model().objects.all(),
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
