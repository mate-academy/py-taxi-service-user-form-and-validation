from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

from taxi.models import Car


class DriverLicenseCreateForm(UserCreationForm):
    license_number = forms.CharField(max_length=8)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        value = self.cleaned_data["license_number"]

        if not re.match(r'^[A-Z]{3}\d{5}$', value):
            raise ValidationError(
                'License must be 3 uppercase letters followed by 5 digits'
            )
        return value


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(max_length=8)


    class Meta:
        model = get_user_model()
        fields = "__all__"

    def clean_license_number(self):
        value = self.cleaned_data["license_number"]

        if not re.match(r'^[A-Z]{3}\d{5}$', value):
            raise ValidationError(
                'License must be 3 uppercase letters followed by 5 digits'
            )
        return value


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = Car
        fields = "__all__"
