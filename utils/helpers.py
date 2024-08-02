import re
import random
import string


def generate_6digit_number() -> int:
    return random.randint(100000, 999999)


def generate_random_string(
    size: int = 6, chars: str = string.ascii_uppercase + string.digits
) -> str:
    return "".join(random.choice(chars) for x in range(size))


def check_identifier_is_email(identifier: str) -> bool:
    """
    Check if the given identifier is a valid email.

    Args:
        identifier (str): The identifier to check.

    Returns:
        bool: True if the identifier is a valid email, False otherwise.
    """
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", identifier) is not None


def normalize_email(email: str) -> str:
    """
    Normalize the email address by lowercasing the domain part of it.
    """
    email = email or ""
    try:
        email_name, domain_part = email.strip().rsplit("@", 1)
    except ValueError:
        pass
    else:
        email = email_name + "@" + domain_part.lower()
    return email


def normalize_phone_number(phone_number: int) -> int:
    """
    Normalize the phone number by removing any special characters or formatting.
    """

    normalized_phone_number = (
        phone_number.replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
        .replace("+", "")
    )
    return normalized_phone_number
