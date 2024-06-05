from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car


class DriverLicenseUpdateForm(forms.ModelForm):  # UserCreationForm

    class Meta:
        model = get_user_model()
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
