"""
Formatting utilities for displaying data.
"""
from datetime import datetime
from typing import Any


def format_date(date_string: str, format: str = "%Y-%m-%d") -> str:
    """Format date string."""
    if not date_string:
        return "N/A"
    try:
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return dt.strftime(format)
    except:
        return date_string


def format_datetime(datetime_string: str, format: str = "%Y-%m-%d %H:%M") -> str:
    """Format datetime string."""
    return format_date(datetime_string, format)


def format_number(number: Any) -> str:
    """Format number with commas."""
    if number is None:
        return "0"
    try:
        return f"{int(number):,}"
    except:
        return str(number)


def format_phone(phone: str) -> str:
    """Format phone number."""
    if not phone:
        return "N/A"
    return phone


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to max length."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
