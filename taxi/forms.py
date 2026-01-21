from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError("Invalid license number the"
                                        " length has to be 8 characters long")
        elif (not license_number[:3].isupper()
              or not license_number[:3].isalpha()):
            raise forms.ValidationError("Invalid license number first 3"
                                        " characters have to "
                                        "be uppercase letters")
        elif not license_number[3:].isdigit():
            raise forms.ValidationError("Invalid license number last 5"
                                        " characters have to be numbers")
        return license_number


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(max_length=8)

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )

    def clean_license_number(self):
        return DriverLicenseUpdateForm.clean_license_number(self)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
