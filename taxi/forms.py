from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(max_length=8, min_length=8)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise forms.ValidationError(
                "The first 3 characters are uppercase letters"
            )
        if not license_number[3:].isdigit():
            raise forms.ValidationError("Last 5 characters are digits")

        return license_number

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
