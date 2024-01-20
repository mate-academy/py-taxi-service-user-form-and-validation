from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )


class DriverLicenseUpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Driver
        fields = ("license_number",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        prefix = license_number[:3]
        ending = license_number[3:]

        if (len(license_number) != 8
                or not prefix.isalpha()
                or not (prefix == prefix.upper())
                or not ending.isdigit()):
            raise forms.ValidationError(
                "Please, enter a valid license number"
            )

        return license_number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
