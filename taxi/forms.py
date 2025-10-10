from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CleanLicenseNumberMixin(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not (license_number[:3].isalpha()
                and license_number[:3].isupper()
                and license_number[3:].isdigit()
                and len(license_number) == 8):
            raise ValidationError("Licence number must be correct")
        return license_number


class DriverCreationForm(CleanLicenseNumberMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(CleanLicenseNumberMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
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
