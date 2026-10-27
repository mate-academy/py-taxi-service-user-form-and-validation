import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

from taxi.models import Car


User = get_user_model()


class DriverCreatForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "License number must be 3 uppercase "
                "letters followed by 5 digits."
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "License number must be 3 uppercase "
                "letters followed by 5 digits."
            )
        return license_number
