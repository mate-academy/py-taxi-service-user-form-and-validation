from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from .models import Car, Driver


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields


class DriverLicenseUpdateForm(forms.ModelForm):

    def clean_license_number(self):
        value = self.cleaned_data["license_number"]
        if len(value) != 8:
            raise ValidationError(
                "Length of licence number must equal to 8"
            )
        if not (value[:3].isalpha() and value[:3].isupper()):
            raise ValidationError(
                "First 3 letters shall be uppercase"
            )
        if not value[3:].isnumeric():
            raise ValidationError(
                "Last 5 symbols shall be digits"
            )
        return value

    class Meta:
        model = Driver
        fields = ["license_number"]


class CarCreateView(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Driver(s)"
    )

    class Meta:
        model = Car
        fields = "__all__"
