from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class LicenseNumberMixin(forms.ModelForm):
    LENGTH = 8
    NUMBER_OF_LETTERS = 3
    NUMBER_OF_DIGITS = -5

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LENGTH:
            raise forms.ValidationError(
                f"Length of license number must be {self.LENGTH}"
            )
        if (license_number[:self.NUMBER_OF_LETTERS]
                != license_number[:self.NUMBER_OF_LETTERS].upper()):
            raise forms.ValidationError("First 3 letters must be uppercase")
        if not license_number[:self.NUMBER_OF_LETTERS].isalpha():
            raise forms.ValidationError("First 3 letters must be letters")
        if not license_number[self.NUMBER_OF_DIGITS:].isdigit():
            raise forms.ValidationError("Last 5 letters must be digits")
        return license_number


class DriverCreationForm(LicenseNumberMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(LicenseNumberMixin, forms.ModelForm):

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
