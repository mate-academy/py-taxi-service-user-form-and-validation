import re

LICENSE_NUMBER_PATTERN = re.compile(r"^[A-Z]{3}\d{5}$")
LICENSE_NUMBER_MESSAGE = (
    "License number must consist of 3 uppercase letters followed by 5 digits."
)
LICENSE_NUMBER_HELP_TEXT = (
    "Enter a license number with 3 uppercase letters followed by 5 digits."
)
