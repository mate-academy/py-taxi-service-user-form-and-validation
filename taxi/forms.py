from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.licence_validation import licence_number_validation
from taxi.models import Driver, Car


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )

    def clean_license_number(self):
        licence_number = self.cleaned_data["license_number"]
        return licence_number_validation(licence_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        licence_number = self.cleaned_data["license_number"]
        return licence_number_validation(licence_number)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
