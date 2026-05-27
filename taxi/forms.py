from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from taxi.models import Car, Driver


def validate_license_number(value: str) -> str:
    if len(value) != 8:
        raise ValidationError(
            "License number must consist of exactly 8 characters."
        )
    if not value[:3].isupper() or not value[:3].isalpha():
        raise ValidationError(
            "First 3 characters of license number must be uppercase letters."
        )
    if not value[3:].isdigit():
        raise ValidationError(
            "Last 5 characters of license number must be digits."
        )
    return value


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number],
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()          # ← was: model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "username",
            Row(
                Column("first_name", css_class="form-group col-md-6"),
                Column("last_name", css_class="form-group col-md-6"),
            ),
            "license_number",
            "password1",
            "password2",
            Submit(
                "submit",
                "Create Driver",
                css_class="btn btn-primary mt-2"),
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number],
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "license_number",
            Submit(
                "submit",
                "Update License",
                css_class="btn btn-primary mt-2",
            ),
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("model", css_class="form-group col-md-6"),
                Column("manufacturer", css_class="form-group col-md-6"),
            ),
            "drivers",
            Submit("submit", "Save", css_class="btn btn-primary mt-2"),
        )
