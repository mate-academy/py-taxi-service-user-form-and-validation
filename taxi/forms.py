from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


class CleanLicenseNumberMixin:
    LEN_LICENSE_NUMBER = 8

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != self.LEN_LICENSE_NUMBER:
            raise forms.ValidationError("Length must be equal to 8")

        first_three = license_number[:3]
        upper_case_chars = first_three.upper()
        last_five_chars = license_number[3:]

        if not (first_three.isalpha() and first_three == upper_case_chars):
            raise forms.ValidationError(
                "Provide correct info "
                "First three chars must be Alphabetic and in UpperCase"
            )
        if not last_five_chars.isnumeric():
            raise forms.ValidationError(
                "Provide correct info "
                "Last five chars must be Numeric"
            )

        return license_number


class CustomUserCreationForm(UserCreationForm, CleanLicenseNumberMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )


class DriverLicenseUpdateForm(forms.ModelForm, CleanLicenseNumberMixin):

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
