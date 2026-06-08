from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):

    license_number = forms.CharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{3}[0-9]{5}$',
            message= '*Number must be only 8 characters'
                     '*First 3 characters are uppercase letter'
                     '*Last 5 characters are digits',
        )]
    )

    class Meta:
        model = Driver
        fields = ['license_number']


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{3}[0-9]{5}$',
            message= '*Number must be only 8 characters'
                     '*First 3 characters are uppercase letter'
                     '*Last 5 characters are digits',
        )]
    )

    class Meta:
        model = Driver
        fields = ('username', 'password', 'first_name', 'last_name', 'license_number')


class CarCreateForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget = forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = ('model', 'manufacturer', 'drivers')
