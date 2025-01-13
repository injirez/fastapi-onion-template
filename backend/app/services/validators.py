import re


def password_complexity_validator(value: str) -> str:
    """
    Password complexity validator
    Requires:
        - number
        - uppercase letter
        - special character
    """
    if not re.findall(r"\d", value):
        raise ValueError("The password must contain at least one number.")

    if not re.findall(r"[A-Z]", value):
        raise ValueError("The password must contain at least one uppercase letter.")

    if not re.findall(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValueError("The password must contain at least one special character.")

    return value
