from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Car


class CleanDriverLicenseMixin(forms.ModelForm):
    LENGHT = 8
    LETTERS_LENGHT = 3
    DIGITS_LENGHT = 5

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        if not (license_number[:self.LETTERS_LENGHT].isupper()
                and license_number[:self.LETTERS_LENGHT].isalpha()):
            raise ValidationError(f"First {self.LETTERS_LENGHT} characters "
                                  "must be uppercased letters")
        if len(license_number) != self.LENGHT:
            raise ValidationError("License number must consist "
                                  f"only of {self.LENGHT} characters!")
        if not license_number[-self.DIGITS_LENGHT:].isdecimal():
            raise ValidationError(f"Last {self.DIGITS_LENGHT} "
                                  "characters must be digits")
        return license_number


class DriverCreationForm(CleanDriverLicenseMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (UserCreationForm.Meta.fields
                  + ("first_name", "last_name", "license_number"))


class DriverLicenseUpdateForm(CleanDriverLicenseMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
