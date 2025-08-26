"""
Utility functions for the Portfolio API application.

This module contains helper functions that can be used across
different parts of the application.
"""

import re
from typing import Optional, Dict, Any
from django.core.exceptions import ValidationError
from django.utils.text import slugify


def validate_url(url: str) -> bool:
    """
    Validate if a string is a valid URL.
    
    Args:
        url (str): The URL string to validate
        
    Returns:
        bool: True if valid URL, False otherwise
    """
    if not url:
        return False
    
    # Basic URL pattern
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url))


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing or replacing invalid characters.
    
    Args:
        filename (str): The original filename
        
    Returns:
        str: The sanitized filename
    """
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove multiple underscores
    filename = re.sub(r'_+', '_', filename)
    # Remove leading/trailing underscores
    filename = filename.strip('_')
    return filename


def format_duration(start_date, end_date=None, current=False) -> str:
    """
    Format a duration between two dates.
    
    Args:
        start_date: Start date
        end_date: End date (optional)
        current (bool): Whether this is a current position
        
    Returns:
        str: Formatted duration string
    """
    if current:
        return f"{start_date.strftime('%b %Y')} - Present"
    
    if not end_date:
        return f"{start_date.strftime('%b %Y')} - Present"
    
    return f"{start_date.strftime('%b %Y')} - {end_date.strftime('%b %Y')}"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text (str): The text to truncate
        max_length (int): Maximum length
        suffix (str): Suffix to add when truncating
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def get_skill_category_display(category: str) -> str:
    """
    Get the human-readable display name for a skill category.
    
    Args:
        category (str): The category code
        
    Returns:
        str: The display name
    """
    category_map = {
        'programming': 'Programming Languages',
        'framework': 'Frameworks & Libraries',
        'database': 'Databases',
        'tool': 'Tools & Technologies',
        'soft': 'Soft Skills',
        'cloud': 'Cloud & DevOps',
        'design': 'Design & UI/UX',
    }
    
    return category_map.get(category, category.title())


def validate_gpa(gpa: float) -> bool:
    """
    Validate GPA value.
    
    Args:
        gpa (float): GPA value to validate
        
    Returns:
        bool: True if valid GPA, False otherwise
    """
    return 0.00 <= gpa <= 4.00


def create_slug(text: str) -> str:
    """
    Create a URL-friendly slug from text.
    
    Args:
        text (str): The text to convert to slug
        
    Returns:
        str: The slug
    """
    return slugify(text)


def get_model_field_help_text(model_class, field_name: str) -> Optional[str]:
    """
    Get help text for a model field.
    
    Args:
        model_class: The Django model class
        field_name (str): Name of the field
        
    Returns:
        Optional[str]: Help text or None if not found
    """
    try:
        field = model_class._meta.get_field(field_name)
        return getattr(field, 'help_text', None)
    except:
        return None


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

