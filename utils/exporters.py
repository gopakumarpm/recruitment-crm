"""
Export utilities for downloading data.
"""
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime


def export_to_csv(data: List[Dict[str, Any]], filename: str = None) -> bytes:
    """
    Export data to CSV format.

    Args:
        data: List of dictionaries to export
        filename: Optional filename (not used, for compatibility)

    Returns:
        CSV data as bytes
    """
    if not data:
        return b""

    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode('utf-8')


def export_to_excel(data: List[Dict[str, Any]], filename: str = None) -> bytes:
    """
    Export data to Excel format.

    Args:
        data: List of dictionaries to export
        filename: Optional filename (not used, for compatibility)

    Returns:
        Excel data as bytes
    """
    if not data:
        return b""

    df = pd.DataFrame(data)

    # Create Excel file in memory
    from io import BytesIO
    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')

    output.seek(0)
    return output.getvalue()


def generate_filename(prefix: str, extension: str) -> str:
    """
    Generate a filename with timestamp.

    Args:
        prefix: Filename prefix
        extension: File extension (csv, xlsx)

    Returns:
        Generated filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"
