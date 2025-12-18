"""
Validation utilities.
"""

import re

# Simple email regex (not RFC 5322 compliant, but good enough for demo)
EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def validate_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: The email address to validate

    Returns:
        True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    return EMAIL_PATTERN.match(email) is not None


def validate_name(name: str, min_length: int = 2, max_length: int = 100) -> bool:
    """
    Validate user name.

    Args:
        name: The name to validate
        min_length: Minimum allowed length
        max_length: Maximum allowed length

    Returns:
        True if valid, False otherwise
    """
    if not name or not isinstance(name, str):
        return False
    stripped = name.strip()
    return min_length <= len(stripped) <= max_length
