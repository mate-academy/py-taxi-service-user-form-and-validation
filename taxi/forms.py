from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import forms
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from taxi.models import Car


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('license_number', 'first_name', 'last_name')

    def clean_license_number(self):
        license_number = self.cleaned_data['license_number']
        if len(license_number) != 8:
            raise ValidationError('License number must be exactly 8 characters!')

        first_three = license_number[:3]
        last_five = license_number[3:]


        if not (first_three.isupper() and first_three.isalpha()):
            raise ValidationError('First 3 characters must be uppercase letters!')

        if not last_five.isdigit():
            raise ValidationError('Last 5 characters must be digits!')

        return license_number

class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('license_number', )

    def clean_license_number(self):
        license_number = self.cleaned_data['license_number']
        if len(license_number) != 8:
            raise ValidationError('License number must be exactly 8 characters!')

        first_three = license_number[:3]
        last_five = license_number[3:]


        if not (first_three.isupper() and first_three.isalpha()):
            raise ValidationError('First 3 characters must be uppercase letters!')

        if not last_five.isdigit():
            raise ValidationError('Last 5 characters must be digits!')

        return license_number

class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"