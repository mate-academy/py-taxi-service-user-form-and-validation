from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ["license_number"]

    # def


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):

        len_license_number = 8
        num_upper_letter = 3
        num_digits = len_license_number - num_upper_letter
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != len_license_number:
            raise ValidationError(f"Length of licence number "
                                  f"should be {len_license_number} symbols")

        if not (license_number[:num_upper_letter].isupper()
                and license_number[:num_upper_letter].isalpha()):
            raise ValidationError(f"First {num_upper_letter} symbols should be"
                                  f" letters in upper case")
        if license_number[num_upper_letter:].isdigit() is False:
            raise ValidationError(
                f"Check your licence number: first {num_digits} "
                f"symbols should be letters in upper case, "
                f"another symbols should be digits"
            )
        return license_number


class DriverForm(DriverLicenseUpdateForm, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = "__all__"

    def clean_license_number(self):
        return super().clean_license_number()


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
