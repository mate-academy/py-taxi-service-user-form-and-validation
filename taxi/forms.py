from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    RIGHT_LICENSE_NUMBER = r"^[A-Z]{3}[0-9]{5}$"
    license_number = forms.RegexField(
        regex=RIGHT_LICENSE_NUMBER)

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (UserCreationForm.Meta.fields + ("first_name",
                                                  "last_name",
                                                  "license_number"))


class DriverLicenseUpdateForm(forms.ModelForm):
    RIGHT_LICENSE_NUMBER = "^[A-Z]{3}[0-9]{5}$"
    license_number = forms.RegexField(regex=RIGHT_LICENSE_NUMBER,)

    class Meta:
        model = Driver
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
