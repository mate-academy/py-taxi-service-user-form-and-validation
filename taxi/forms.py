from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


class Mixin(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if license_number[:3].isalpha() is False:
            raise forms.ValidationError("Invalid license number."
                                        "First 3 characters"
                                        " must be alphanumeric")

        if license_number[:3] != license_number[:3].upper():
            raise forms.ValidationError("Invalid license number."
                                        " First 3 characters"
                                        " must be uppercase letter")

        if license_number[-5:].isdigit() is not True:
            raise forms.ValidationError("Invalid license number."
                                        " Last 5 characters must be digits")

        return license_number


class DriverCreationForm(UserCreationForm, Mixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",
                                                 "first_name",
                                                 "last_name", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False)

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(Mixin):
    class Meta:
        model = Driver
        fields = ["license_number"]
