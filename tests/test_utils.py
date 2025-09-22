"""
Tests for utility functions.
"""

import sys
import unittest
from unittest.mock import patch
import os

# Add src to path for imports
sys.path.insert(0, '.')

from src.utils.helpers import (
    setup_logger, validate_input, safe_get_env, 
    timestamp, sanitize_string
)


class TestHelpers(unittest.TestCase):
    """Test cases for helper utilities."""
    
    def test_validate_input_success(self):
        """Test successful input validation."""
        result = validate_input("test", str, "test_field")
        self.assertTrue(result)
    
    def test_validate_input_failure(self):
        """Test input validation failure."""
        with self.assertRaises(TypeError):
            validate_input(123, str, "test_field")
    
    def test_sanitize_string_basic(self):
        """Test basic string sanitization."""
        result = sanitize_string("  hello world  ")
        self.assertEqual(result, "hello world")
    
    def test_sanitize_string_dangerous_chars(self):
        """Test sanitization of dangerous characters."""
        dangerous_input = "<script>alert('xss')</script>"
        result = sanitize_string(dangerous_input)
        self.assertNotIn("<", result)
        self.assertNotIn(">", result)
    
    def test_sanitize_string_too_long(self):
        """Test sanitization with string too long."""
        long_string = "a" * 1001
        with self.assertRaises(ValueError):
            sanitize_string(long_string)
    
    def test_sanitize_string_invalid_type(self):
        """Test sanitization with invalid input type."""
        with self.assertRaises(ValueError):
            sanitize_string(123)
    
    def test_timestamp_format(self):
        """Test timestamp format."""
        ts = timestamp()
        self.assertIsInstance(ts, str)
        # Should be ISO format with 'T' separator
        self.assertIn('T', ts)
    
    @patch.dict(os.environ, {'TEST_VAR': 'test_value'})
    def test_safe_get_env_existing(self):
        """Test getting existing environment variable."""
        result = safe_get_env('TEST_VAR')
        self.assertEqual(result, 'test_value')
    
    def test_safe_get_env_default(self):
        """Test getting non-existing environment variable with default."""
        result = safe_get_env('NON_EXISTING', 'default_value')
        self.assertEqual(result, 'default_value')
    
    def test_safe_get_env_required_missing(self):
        """Test required environment variable that's missing."""
        with self.assertRaises(ValueError):
            safe_get_env('NON_EXISTING_REQUIRED', required=True)
    
    def test_setup_logger(self):
        """Test logger setup."""
        logger = setup_logger('test_logger', 'DEBUG')
        self.assertEqual(logger.name, 'test_logger')


if __name__ == '__main__':
    unittest.main()