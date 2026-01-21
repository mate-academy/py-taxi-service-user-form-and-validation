from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Driver, Car


class CarUpdateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),                                              # noqa
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )

    def clean_license_number(self):
        license = self.cleaned_data['license_number']

        if (len(license) != 8
                or
                not license[:3].isalpha()
                or
                not license[:3].isupper()
                or
                not license[-5:].isdigit()):
            raise forms.ValidationError('Invalid license number!')

        return license


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ['license_number']

    def clean_license_number(self):
        license = self.cleaned_data['license_number']

        if (len(license) != 8
                or
                not license[:3].isalpha()
                or
                not license[:3].isupper()
                or
                not license[-5:].isdigit()):
            raise forms.ValidationError('Invalid license number!')

        return license
