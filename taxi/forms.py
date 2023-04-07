from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class LicenseMixin:
    def clean_license_number(self) -> str:
        l_num = self.cleaned_data["license_number"]
        if len(l_num) != 8:
            raise ValidationError("License should consist only 8 characters")
        elif l_num[:3].isalpha() is False or l_num[:3] != l_num[:3].upper():
            raise ValidationError("First 3 char should be uppercase letters")
        elif l_num[3:].isnumeric() is False:
            raise ValidationError("Last 5 char should be digits")
        return l_num


class DriverCreationForm(UserCreationForm, LicenseMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )


class DriverLicenseUpdateForm(forms.ModelForm, LicenseMixin):
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


class CarDriverUpdateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = []
        widgets = {
            "id": forms.HiddenInput(),
            "drivers": forms.HiddenInput(),
        }
