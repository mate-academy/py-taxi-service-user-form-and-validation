from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class LicenseNumberMixin(forms.Form):
    LICENSE_NUMBER_LEN = 8
    UPPERCASE_NUM = 3
    DIGIT_NUM = 5

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LICENSE_NUMBER_LEN:
            raise forms.ValidationError(
                "The lenght of license number must be 8."
            )

        if (not license_number[:self.UPPERCASE_NUM].isalpha() or not
                license_number[self.UPPERCASE_NUM:].isdigit()):
            raise forms.ValidationError(
                "The first 3 characters must be in uppercase letters."
                "The last 5 characters must be digits.")

        return license_number


class DriverCreationForm(UserCreationForm, LicenseNumberMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class DriverLicenseUpdateForm(forms.ModelForm, LicenseNumberMixin):
    class Meta:
        model = get_user_model()
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
