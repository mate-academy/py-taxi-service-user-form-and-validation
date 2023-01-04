from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.shortcuts import redirect

from taxi.models import Driver, Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect("taxi:car-detail", self.object.pk)


class DriverCreationForm(UserCreationForm):

    first_name = forms.CharField(max_length=63, required=True)
    last_name = forms.CharField(max_length=63, required=True)

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):

    @staticmethod
    def license_length_validator(value):
        license_ = str(value)
        if len(license_) != 8:
            raise forms.ValidationError("Ensure this value has 8 characters.")

    @staticmethod
    def license_content_validator(value):
        license_ = str(value)

        should_be_upper_chars = license_[:3]
        should_be_digits = license_[3:]

        if not (all([
            should_be_upper_chars.isalpha(),
            should_be_upper_chars.isupper()
        ])):
            raise forms.ValidationError(
                "First 3 characters should be uppercase letters."
            )

        if not (should_be_digits.isdigit()):
            raise forms.ValidationError(
                "Last 5 characters should be digits."
            )

    license_number = forms.CharField(
        max_length=255,
        validators=[license_length_validator, license_content_validator]
    )

    class Meta:
        model = Driver
        fields = ["license_number"]
