from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car


class DriveUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "Ensure that the length of the password is 8 characters"
            )
        if not license_number[:3].isupper():
            raise ValidationError(
                "Ensure that first three letters are capital letters"
            )
        if not license_number[:3].isalpha():
            raise ValidationError(
                "Ensure that first three letters are letters"
            )
        if not license_number[3:].isnumeric():
            raise ValidationError(
                "Ensure that last five characters are numbers"
            )
        return license_number
