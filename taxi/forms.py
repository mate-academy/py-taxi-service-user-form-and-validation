from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseRequiredMixin(forms.ModelForm):

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("Please enter correct license number.")

        if not (license_number[:3].isupper() and license_number[:3].isalpha()):
            raise ValidationError("Please enter correct license number.")

        if not license_number[-5:].isdigit():
            raise ValidationError("Please enter correct license number.")

        return license_number


class DriverCreationForm(DriverLicenseRequiredMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )


class DriverLicenseUpdateForm(DriverLicenseRequiredMixin, forms.ModelForm):
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


class CarDriverForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ()
