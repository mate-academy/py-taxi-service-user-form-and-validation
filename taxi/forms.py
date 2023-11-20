from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import (ModelForm,
                          ModelMultipleChoiceField,
                          CheckboxSelectMultiple)

from taxi.models import Driver, Car
from taxi.validators import license_number_validator


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name",
                                                 "last_name",
                                                 "license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        license_number_validator(license_number)
        return license_number


class DriverLicenseUpdateForm(ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        license_number_validator(license_number)
        return license_number


class CarForm(ModelForm):
    drivers = ModelMultipleChoiceField(queryset=get_user_model().objects.all(),
                                       widget=CheckboxSelectMultiple,
                                       required=False)

    class Meta:
        model = Car
        fields = "__all__"
