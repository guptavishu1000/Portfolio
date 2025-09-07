"""
Constants and configuration values for the portfolio API.
"""

# Skill Categories
SKILL_CATEGORIES = [
    ('programming', 'Programming Languages'),
    ('framework', 'Frameworks & Libraries'),
    ('database', 'Databases'),
    ('tool', 'Tools & Technologies'),
    ('soft', 'Soft Skills'),
    ('cloud', 'Cloud & DevOps'),
    ('design', 'Design & UI/UX'),
]

# Proficiency Levels
PROFICIENCY_CHOICES = [(i, f"{i}/10") for i in range(1, 11)]

# GPA Validation
GPA_MIN = 0.00
GPA_MAX = 4.00

# File Upload Paths
UPLOAD_PATHS = {
    'profile': 'media/profile/',
    'resume': 'media/resume/',
    'projects': 'media/projects/',
}

# API Configuration
API_VERSION = '1.0.0'
API_TITLE = 'Portfolio API'
API_DESCRIPTION = 'A comprehensive API for managing portfolio information'

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Contact Form
CONTACT_SUCCESS_MESSAGE = 'Thank you for your message! I will get back to you soon.'
CONTACT_ERROR_MESSAGE = 'Error creating contact message: {}'

# Validation Messages
VALIDATION_MESSAGES = {
    'end_date_before_start': 'End date cannot be before start date',
    'current_with_end_date': 'Current position should not have an end date',
    'only_one_personal_info': 'Only one PersonalInfo instance can exist',
}

