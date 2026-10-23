from django import forms
from django.contrib.auth.forms import UserCreationForm
from taxi.models import Driver, Car
from django.core.exceptions import ValidationError


class DriverUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("first_name", "last_name", "license_number", ))

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if (len(license_number) != 8
                or license_number[0:3] != license_number[0:3].upper()
                or not license_number[0:3].isalpha()
                or not license_number[3:].isdigit()):
            raise ValidationError("Invalid license number")
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)
        labels = {"license_number": ""}

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if (len(license_number) != 8
                or license_number[0:3] != license_number[0:3].upper()
                or not license_number[0:3].isalpha()
                or not license_number[3:].isdigit()):
            raise ValidationError("Invalid license number")
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Car
        fields = "__all__"
