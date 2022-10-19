from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number", "username", "first_name", "last_name")

    def clean_license_number(self):

        license_number = self.cleaned_data["license_number"]
        print(license_number[3].upper())
        if not len(license_number) == 8:
            raise ValidationError("Length must be 8 symbols")
        if not license_number[0:3].upper() == license_number[0:3]:
            raise ValidationError("The first 3 symbols must be in upper case letters")
        first_part = license_number[0:3]
        if len ([el for el in first_part if not el.isalpha()]) > 0:
            raise ValidationError ("The first 3 symbols must be in upper case letters")
        end_part = license_number[-5:]
        if len([el for el in end_part if not el.isdigit()]) > 0:
            raise ValidationError("Last 5 symbols must be as digit")

        return license_number


class DriverLicenseUpdateForm(DriverForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    # def clean_license_number(self):
    #
    #     license_number = self.cleaned_data["license_number"]
    #     print(license_number[3].upper())
    #     if not len(license_number) == 8:
    #         raise ValidationError("Length must be 8 symbols")
    #     if not license_number[0:3].upper() == license_number[0:3]:
    #         raise ValidationError("The first 3 symbols must be in upper case letters")
    #     first_part = license_number[0:3]
    #     if len ([el for el in first_part if not el.isalpha()]) > 0:
    #         raise ValidationError ("The first 3 symbols must be in upper case letters")
    #     end_part = license_number[-5:]
    #     if len([el for el in end_part if not el.isdigit()]) > 0:
    #         raise ValidationError("Last 5 symbols must be as digit")
    #
    #     return license_number



class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
