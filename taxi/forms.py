from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car
from django import forms


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise forms.ValidationError("Length of license number "
                                    "must be equal to 8!")
    if not (license_number[:3].isalpha() and license_number[:3].isupper()):
        raise forms.ValidationError("First 3 symbols "
                                    "must be letters and upper!")
    if not license_number[3:].isdigit():
        raise forms.ValidationError("Last 5 symbols "
                                    "must be digits!")

    return license_number


class DriverCreationForm(UserCreationForm):

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarsForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
