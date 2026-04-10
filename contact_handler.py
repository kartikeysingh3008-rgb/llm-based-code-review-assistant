import re


def is_valid_gmail(email: str) -> bool:
    if not email:
        return False
    return bool(re.match(r'^[^@\s]+@gmail\.com$', email.strip(), re.IGNORECASE))


def validate_contact_form(name: str, email: str, message: str) -> tuple[bool, str]:
    if not name or not email or not message:
        return False, "Please fill in all required fields."
    if not is_valid_gmail(email):
        return False, "Please use a valid Gmail address ending in @gmail.com."
    return True, f"Message sent: \"{message.strip()}\""
