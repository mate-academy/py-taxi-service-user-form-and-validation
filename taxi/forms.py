from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car
from taxi.validators import clean_license_number


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(validators=[clean_license_number])

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(validators=[clean_license_number])

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Car
        fields = "__all__"
