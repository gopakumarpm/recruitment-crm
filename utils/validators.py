"""
Validation utilities for form inputs.
"""
import re
from typing import Tuple
from email_validator import validate_email, EmailNotValidError


def validate_email_address(email: str) -> Tuple[bool, str]:
    """
    Validate email address.

    Args:
        email: Email address to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"

    try:
        validate_email(email)
        return True, ""
    except EmailNotValidError as e:
        return False, str(e)


def validate_phone(phone: str) -> Tuple[bool, str]:
    """
    Validate phone number.

    Args:
        phone: Phone number to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not phone:
        return True, ""  # Phone is optional

    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)

    # Check if it contains only digits and is of reasonable length
    if not cleaned.isdigit() or len(cleaned) < 7 or len(cleaned) > 15:
        return False, "Invalid phone number format"

    return True, ""


def validate_url(url: str) -> Tuple[bool, str]:
    """
    Validate URL.

    Args:
        url: URL to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not url:
        return True, ""  # URL is optional

    # Basic URL pattern
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not url_pattern.match(url):
        return False, "Invalid URL format. Must start with http:// or https://"

    return True, ""


def validate_required_field(value: any, field_name: str) -> Tuple[bool, str]:
    """
    Validate required field.

    Args:
        value: Field value
        field_name: Name of the field

    Returns:
        Tuple of (is_valid, error_message)
    """
    if value is None or (isinstance(value, str) and not value.strip()):
        return False, f"{field_name} is required"

    return True, ""


def validate_number_range(value: any, min_val: int = None, max_val: int = None,
                         field_name: str = "Value") -> Tuple[bool, str]:
    """
    Validate number is within range.

    Args:
        value: Value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        field_name: Name of the field

    Returns:
        Tuple of (is_valid, error_message)
    """
    if value is None or value == "":
        return True, ""  # Optional

    try:
        num_value = int(value) if isinstance(value, str) else value

        if min_val is not None and num_value < min_val:
            return False, f"{field_name} must be at least {min_val}"

        if max_val is not None and num_value > max_val:
            return False, f"{field_name} must be at most {max_val}"

        return True, ""

    except (ValueError, TypeError):
        return False, f"{field_name} must be a number"


def validate_candidate_data(data: dict) -> Tuple[bool, list]:
    """
    Validate candidate data.

    Args:
        data: Candidate data dictionary

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Required fields
    is_valid, error = validate_required_field(data.get('first_name'), "First name")
    if not is_valid:
        errors.append(error)

    is_valid, error = validate_required_field(data.get('last_name'), "Last name")
    if not is_valid:
        errors.append(error)

    # Email validation
    is_valid, error = validate_email_address(data.get('email', ''))
    if not is_valid:
        errors.append(error)

    # Phone validation
    if data.get('phone'):
        is_valid, error = validate_phone(data.get('phone'))
        if not is_valid:
            errors.append(error)

    # URL validations
    if data.get('linkedin_url'):
        is_valid, error = validate_url(data.get('linkedin_url'))
        if not is_valid:
            errors.append(f"LinkedIn URL: {error}")

    if data.get('resume_url'):
        is_valid, error = validate_url(data.get('resume_url'))
        if not is_valid:
            errors.append(f"Resume URL: {error}")

    # Experience validation
    if data.get('years_of_experience') is not None:
        is_valid, error = validate_number_range(
            data.get('years_of_experience'),
            min_val=0,
            max_val=70,
            field_name="Years of experience"
        )
        if not is_valid:
            errors.append(error)

    return len(errors) == 0, errors


def validate_user_data(data: dict, is_update: bool = False) -> Tuple[bool, list]:
    """
    Validate user data.

    Args:
        data: User data dictionary
        is_update: Whether this is an update operation

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Required fields
    is_valid, error = validate_required_field(data.get('username'), "Username")
    if not is_valid and not is_update:
        errors.append(error)

    is_valid, error = validate_required_field(data.get('full_name'), "Full name")
    if not is_valid:
        errors.append(error)

    # Email validation
    is_valid, error = validate_email_address(data.get('email', ''))
    if not is_valid:
        errors.append(error)

    # Password validation (only for new users or password change)
    if not is_update and data.get('password'):
        password = data.get('password')
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")

    return len(errors) == 0, errors
