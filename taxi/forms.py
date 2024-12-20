from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be 8 symbols long"
            )
        elif not (
                license_number[:3].isalpha() and license_number[:3].isupper()
        ):
            raise forms.ValidationError(
                "License number should start with 3 letters in uppercase"
            )
        elif not license_number[3:].isnumeric():
            raise forms.ValidationError(
                "License number should finish with 5 numbers"
            )

        return license_number


class DriverCreateForm(UserCreationForm, DriverLicenseUpdateForm):
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
