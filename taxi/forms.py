from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views import generic

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

        LEN_LICENSE_NUMBER = 8
        NUM_UPPER_LETTERS = 3
        NUM_DIGITS = LEN_LICENSE_NUMBER - NUM_UPPER_LETTERS
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != LEN_LICENSE_NUMBER:
            raise ValidationError(f"Lenght of licence number should be {LEN_LICENSE_NUMBER} symbols")

        if not (license_number[:NUM_UPPER_LETTERS].isupper() and license_number[:NUM_UPPER_LETTERS].isalpha()):
            raise ValidationError(f"First {NUM_UPPER_LETTERS} symbols should be"
                                  f" letters in upper case")
        if license_number[NUM_UPPER_LETTERS:].isdigit() is False:
            raise ValidationError(
                f"Check your licence number: first {NUM_UPPER_LETTERS} symbols should be"
                f" letters in upper case, another symbols should be digits"
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
