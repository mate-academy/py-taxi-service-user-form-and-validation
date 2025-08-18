import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car

User = get_user_model()

class CleanLicenseNumberMixin(forms.Form):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise ValidationError(
                "License number must consist only of 8 characters "
                "First 3 characters are uppercase letters "
                "Last 5 characters are digits"
            )
        return license_number


class DriverForm(CleanLicenseNumberMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(CleanLicenseNumberMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
