from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    # def clean(self):
    #     license_number = self.cleaned_data["license_number"]
    #     validators = [
    #         len(license_number) == 8,
    #         license_number[:3].isupper(),
    #         license_number[3:].isdigit()
    #     ]
    #     for validator in validators:
    #         if not validator:
    #             raise ValidationError(
    #                 "Enter correct license number"
    #             )
    #     return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
