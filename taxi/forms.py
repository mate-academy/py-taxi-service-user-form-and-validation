from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class BaseLicenseForm(forms.ModelForm):
    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "License number must contain 8 symbols"
            )
        if (not license_number[0:3].isupper()
                or not license_number[:3].isalpha()):
            raise ValidationError("First 3 characters must be uppercase")
        if not license_number[-5:].isdigit():
            raise ValidationError("Last 5 characters must be digits")
        return license_number


class DriverCreation(BaseLicenseForm, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )


class DriverLicenseUpdateForm(BaseLicenseForm, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )
        template_name = "taxi/driver_license_update.html"


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
