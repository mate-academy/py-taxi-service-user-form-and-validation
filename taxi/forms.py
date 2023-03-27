from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        num = self.cleaned_data["license_number"]
        if len(num) != 8 or not num[:3].isupper() or not num[3:].isdigit():
            raise ValidationError(
                "License Number must consist only of 8 chars,"
                " first 3 chars must be in uppercase,"
                " last 3 must be digits")
        return num


class DriverForm(UserCreationForm, DriverLicenseUpdateForm):
    class Meta:
        model = Driver
        fields = ("username",
                  "first_name",
                  "last_name",
                  "license_number",
                  "email",)

    def clean_license_number(self):
        return super().clean_license_number()


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
