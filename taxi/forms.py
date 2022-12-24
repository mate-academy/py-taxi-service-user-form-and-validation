from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("License number must consist 8 symbols")

        if license_number[0:3].isalpha() is False:
            raise ValidationError("First three symbols are letters")

        if license_number[0:3].upper() != license_number[0:3]:
            raise ValidationError("First three symbols are uppercase letters")

        if license_number[3:].isdigit() is False:
            raise ValidationError("From 4th to 8th symbols are digits")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False

    )

    class Meta:
        model = Car
        fields = "__all__"
