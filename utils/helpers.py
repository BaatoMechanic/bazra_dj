import re
import random


def generate_6digit_number():
    return random.randint(100000, 999999)


def check_identifier_is_email(identifier: str) -> bool:
    """
    Check if the given identifier is a valid email.

    Args:
        identifier (str): The identifier to check.

    Returns:
        bool: True if the identifier is a valid email, False otherwise.
    """
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', identifier) is not None



