from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class DriverCreationForm(UserCreationForm):

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverUpdateLicenseForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        string = [letter for letter in str(license_number)]

        if len(string) != 8:
            raise ValidationError(
                "make sure that license number consist only of 8 characters")

        for letter in string[:3]:
            if not letter.isalpha():
                raise ValidationError("make sure that license number"
                                      " consist first 3 alphabet letters ")
            if letter.islower():
                raise ValidationError("make sure that license number"
                                      " consist first 3 uppercase alphabet letters ")

        for letter in string[3:]:
            if not letter.isnumeric():
                raise ValidationError("make sure that license number"
                                      " consist last 5 digit characters")

        return license_number

