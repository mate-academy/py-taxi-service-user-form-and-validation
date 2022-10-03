from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverUpdateLicenseForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ('license_number',)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) == 8 and license_number[0:4].isupper() and license_number[3:].isdigit():
            return license_number
        raise ValidationError("Input correct credentials!")


class DriverCreateForm(UserCreationForm, DriverUpdateLicenseForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number")


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
