from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'license_number')


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['license_number']

    def clean_license_number(self):
        value = self.cleaned_data['license_number']
        if len(value) != 8:
            raise forms.ValidationError("License number must be exactly 8 characters.")
        if not value[:3].isalpha() or not value[:3].isupper():
            raise forms.ValidationError("First 3 characters must be uppercase letters.")
        if not value[3:].isdigit():
            raise forms.ValidationError("Last 5 characters must be digits.")
        return value


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
