from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class LicenseNumberMixin:
    def clean_license_number(self):
        license_num = self.cleaned_data.get("license_number")
        if len(license_num) != 8:
            raise forms.ValidationError("Length of license number must be only 8 characters")
        if not license_num[:3].isalpha() or not license_num[:3].isupper():
            raise forms.ValidationError("First 3 characters must be uppercase letters")
        if not license_num[3:].isdigit():
            raise forms.ValidationError("Last 5 characters must be digits")
        return license_num


class DriverCreationForm(LicenseNumberMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )


class DriverLicenseUpdateForm(LicenseNumberMixin, forms.ModelForm):
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
