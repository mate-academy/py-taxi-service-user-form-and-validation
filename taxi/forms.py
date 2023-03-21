from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        # fields = UserCreationForm.Meta.fields + ()


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        print(license_number[0:3])
        if len(license_number) != 8:
            raise ValidationError("Ensure that number of character equals to 8")

        if license_number[0:3] != license_number[0:3].upper():
            raise ValidationError("First 3 character should be uppercase letters")
        try:
            int(license_number[3:])
        except:
            raise ValidationError("Last 5 character should be digits")
        return license_number
