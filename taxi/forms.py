from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Driver, Car


class BaseDriverForm(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if (len(license_number) != 8
                or not license_number[:3].isalpha()
                or not license_number[:3].isupper()
                or not license_number[3:].isdigit()):
            raise ValidationError("Remember the rules:"
                                  "First 3 symbols are uppercase letters"
                                  "4-8 symbols are digits")
        return license_number


class DriverForm(BaseDriverForm):
    class Meta:
        model = Driver
        fields = "__all__"


class DriverLicenseUpdateForm(BaseDriverForm):
    class Meta:
        model = Driver
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
