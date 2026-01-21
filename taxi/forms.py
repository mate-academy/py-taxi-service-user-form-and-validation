from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        if not len(self.cleaned_data["license_number"]) == 8:
            raise ValidationError("license number must"
                                  " consist only 8 charactrers")
        if (not self.cleaned_data["license_number"][:3]
                != self.cleaned_data["license_number"][:3].upper()
                and not self.cleaned_data["license_number"][:3].isalpha()):
            raise ValidationError("first 3 char must be uppercase letters")
        if not self.cleaned_data["license_number"][-5:].isdigit():
            raise ValidationError("last 5 char must be int")
        return self.cleaned_data["license_number"]


class DriverCreateForm(DriverLicenseUpdateForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
