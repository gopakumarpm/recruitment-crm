"""
Configuration settings for the Recruitment CRM application.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Database settings
DATABASE_DIR = BASE_DIR / "data"
DATABASE_PATH = DATABASE_DIR / "recruitment.db"

# Ensure data directory exists
DATABASE_DIR.mkdir(exist_ok=True)

# Application settings
APP_NAME = "Recruitment CRM"
APP_VERSION = "1.0.0"

# Session settings
SESSION_TIMEOUT_HOURS = 24

# Default admin credentials (change on first login)
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"
DEFAULT_ADMIN_EMAIL = "admin@recruitment-crm.com"

# Pagination
RECORDS_PER_PAGE = 50

# Export settings
EXPORT_DIR = BASE_DIR / "exports"
EXPORT_DIR.mkdir(exist_ok=True)

# Logging
LOG_LEVEL = "INFO"
