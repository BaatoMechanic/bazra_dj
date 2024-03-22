import re
import random
import string


def generate_6digit_number():
    return random.randint(100000, 999999)


def generate_random_string(size=6, chars=string.ascii_uppercase + string.digits):
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
