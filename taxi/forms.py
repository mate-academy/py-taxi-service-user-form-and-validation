from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from taxi.models import Driver, Car


class DriverForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name")


class DriverLicenseUpdateForm (forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number should contain 8 letters"
            )
        if not license_number[:3:].isalpha():
            raise forms.ValidationError(
                "The first 3 symbols should be letters"
            )
        if not license_number[:3:].isupper():
            raise forms.ValidationError(
                "The first 3 symbols should be uppercase letters"
            )
        if not license_number[3::].isdigit():
            raise forms.ValidationError(
                "The last 5 symbols should be digits"
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
