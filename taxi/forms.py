from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):

    def clean_license_number(self):
        data = self.cleaned_data["license_number"]

        if not len(data) == 8:
            raise forms.ValidationError(
                "Length of license number should be equal 8"
            )

        for character in data[0:3]:
            if not character.isupper():
                raise forms.ValidationError(
                    "The first 3 characters should be uppercase letters."
                )

        for character in data[-5:-1]:
            if not character.isdigit():
                raise forms.ValidationError(
                    "The last 5 characters must be numbers."
                )
        return data

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
