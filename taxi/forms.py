from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = get_user_model().license_number

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        first_three_letters = license_number[:3]
        second_five_digits = license_number[3:]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number should consist only of 8 characters"
            )
        if (not first_three_letters.isupper()
                or not first_three_letters.isalpha()):
            raise forms.ValidationError(
                "First three letters should be uppercase letters"
            )
        if not second_five_digits.isdigit():
            raise forms.ValidationError("Second five digits should be digits")
        return license_number

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
