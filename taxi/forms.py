from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    MAX_LEN = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverLicenseUpdateForm.MAX_LEN:
            raise ValidationError(
                f"Ensure that length of license number "
                f"is < than {DriverLicenseUpdateForm.MAX_LEN}!"
            )

        license_number_triad = license_number[:3]
        is_lower = license_number_triad.islower()
        is_str = isinstance(license_number_triad, str)
        is_num = False
        num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for num_ in num:
            if str(num_) in license_number_triad:
                is_num = True

        if is_lower or not is_str or is_num:
            raise ValidationError(
                "Ensure that your letters are uppercase!"
            )

        try:
            isinstance(int(license_number[3:8]), int)
        except ValueError:
            raise ValidationError(
                "Your last 5 characters must be digits!"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
