"""Utility functions - better code quality."""


def sanitize_input(user_input):
    """Sanitize user input (good practice)."""
    # Remove dangerous characters
    dangerous_chars = ['<', '>', '"', "'", ';', '&', '|']
    sanitized = user_input
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized


def validate_email(email):
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# GOOD: Using environment variable for secrets
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///default.db')
