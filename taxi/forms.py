from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ("username", "license_number", "password1", "password2")


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = get_user_model()
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta(forms.ModelForm):
        model = Car
        fields = ("model", "manufacturer", "drivers")
