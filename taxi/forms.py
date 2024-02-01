from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )
        help_texts = {
            "license_number": "<ul>"
                              "<li>Consist only of 8 characters</li>"
                              "<li>"
                              "First 3 characters are uppercase letters"
                              "</li>"
                              "<li>Last 5 characters are digits</li>"
                              "</ul>"
        }


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]
        help_texts = {
            "license_number": "<ul>"
                              "<li>Consist only of 8 characters</li>"
                              "<li>"
                              "First 3 characters are uppercase letters"
                              "</li>"
                              "<li>Last 5 characters are digits</li>"
                              "</ul>"
        }
        template_name = "taxi/driver_license_update_form.html"


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
