from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseValidationMixin(forms.ModelForm):

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("Must consist only of 8 characters")
        first_3: str = license_number[:3]
        if not (first_3.isalpha() and first_3.isupper()):
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )
        if not license_number[-5:].isdigit():
            raise ValidationError("Last 5 characters must be digits")
        return license_number


class DriverCreationForm(DriverLicenseValidationMixin, UserCreationForm):

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(DriverLicenseValidationMixin, forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
