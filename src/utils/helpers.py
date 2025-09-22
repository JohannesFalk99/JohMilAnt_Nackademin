"""
Helper utilities for JohMilAnt_Nackademin.
"""

import logging
from typing import Any, Optional
from datetime import datetime


def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Set up a logger with specified name and level.
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    logger.setLevel(getattr(logging, level.upper()))
    return logger


def validate_input(value: Any, expected_type: type, field_name: str) -> bool:
    """
    Validate input value against expected type.
    
    Args:
        value: Value to validate
        expected_type: Expected type
        field_name: Name of the field being validated
        
    Returns:
        True if valid, False otherwise
        
    Raises:
        TypeError: If validation fails
    """
    if not isinstance(value, expected_type):
        raise TypeError(
            f"Invalid type for {field_name}. "
            f"Expected {expected_type.__name__}, got {type(value).__name__}"
        )
    return True


def safe_get_env(key: str, default: Optional[str] = None, 
                 required: bool = False) -> Optional[str]:
    """
    Safely get environment variable with validation.
    
    Args:
        key: Environment variable key
        default: Default value if not found
        required: Whether the variable is required
        
    Returns:
        Environment variable value or default
        
    Raises:
        ValueError: If required variable is not found
    """
    import os
    
    value = os.getenv(key, default)
    
    if required and value is None:
        raise ValueError(f"Required environment variable '{key}' not found")
    
    return value


def timestamp() -> str:
    """
    Get current timestamp as string.
    
    Returns:
        Current timestamp in ISO format
    """
    return datetime.now().isoformat()


def sanitize_string(text: str, max_length: int = 1000) -> str:
    """
    Sanitize string input to prevent injection attacks.
    
    Args:
        text: Text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
        
    Raises:
        ValueError: If text is too long or invalid
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    
    if len(text) > max_length:
        raise ValueError(f"Text too long. Maximum {max_length} characters allowed")
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', '%', ';']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()