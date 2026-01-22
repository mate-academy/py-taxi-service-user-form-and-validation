from django.core.validators import RegexValidator

license_number_validator = RegexValidator(
    regex="^[A-Z]{3}[0-9]{5}$",
    message="License number should consist "
            "only 8 characters where "
            "first 3 characters are uppercase letters and "
            "last 5 characters are digits."
)
