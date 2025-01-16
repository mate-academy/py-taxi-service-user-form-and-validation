from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from taxi.models import Driver, Car


class DriverForm(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) < 8:
            raise forms.ValidationError("License number is too short")
        elif len(license_number) > 8:
            raise forms.ValidationError("License number is too long")
        elif not license_number[:3].isalpha():
            raise forms.ValidationError("First 3 characters must be letters")
        elif not license_number[3:].isnumeric():
            raise forms.ValidationError("Last 5 characters must be numeric")
        elif not license_number[:3].isupper():
            raise forms.ValidationError("Letters should be uppercase")
        return license_number


class DriverCreationForm(UserCreationForm, DriverForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )


class DriverLicenseUpdateForm(UserChangeForm, DriverForm):
    class Meta:
        model = Driver
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
