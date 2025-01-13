import re


def password_complexity_validator(value: str) -> str:
    if not re.findall(r"\d", value):
        raise ValueError("The password must contain at least one number.")

    if not re.findall(r"[a-z]", value):
        raise ValueError("The password must contain at least one lowercase letter.")

    if not re.findall(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValueError("The password must contain at least one special character.")

    return value
