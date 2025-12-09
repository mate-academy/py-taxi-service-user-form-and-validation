import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_license_number(value: str):
    pattern = r"^[A-Z]{3}\d{5}$"
    if not re.match(pattern, value):
        raise ValidationError(
            _("License number must be 3 uppercase "
              "letters followed by 5 digits (8 characters total)."),
            code="invalid_license_number",
        )
