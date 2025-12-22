from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


class DriverCreateForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not license_number:
            raise forms.ValidationError("The field cannot be empty")

        if len(license_number) != 8:
            raise forms.ValidationError("The field must have 8 characters")

        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise forms.ValidationError(
                "The first 3 letters must be capitalized")

        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "The last 5 characters must be numbers")

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not license_number:
            raise forms.ValidationError("The field cannot be empty")

        if len(license_number) != 8:
            raise forms.ValidationError("The field must have 8 characters")

        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise forms.ValidationError(
                "The first 3 letters must be capitalized")

        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "The last 5 characters must be numbers")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
