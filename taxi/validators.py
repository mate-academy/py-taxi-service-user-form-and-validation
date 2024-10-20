from django.core.validators import RegexValidator


class LicenseNumberValidator(RegexValidator):
    regex = r"^[A-Z]{3}\d{5}$"
    message = (
        "License number must consist of 3 uppercase letters followed "
        "by 5 digits."
    )
