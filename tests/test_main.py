"""
Tests for main.py functionality.
"""

import sys
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

# Add src to path for imports
sys.path.insert(0, '.')

import main


class TestMain(unittest.TestCase):
    """Test cases for main module."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.original_stdout = sys.stdout
        self.captured_output = StringIO()
        
    def tearDown(self):
        """Clean up after each test method."""
        sys.stdout = self.original_stdout
    
    def test_main_success(self):
        """Test successful execution of main function."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            result = main.main()
            
        self.assertEqual(result, 0)
        self.assertIn("Hello, JohMilAnt_Nackademin!", mock_stdout.getvalue())
    
    @patch('main.logger')
    def test_main_with_exception(self, mock_logger):
        """Test main function behavior when an exception occurs."""
        with patch('builtins.print', side_effect=Exception("Test error")):
            result = main.main()
            
        self.assertEqual(result, 1)
        mock_logger.error.assert_called_once()
    
    @patch('main.logger')
    def test_logging_calls(self, mock_logger):
        """Test that appropriate logging calls are made."""
        main.main()
        
        # Check that info logs were called
        mock_logger.info.assert_any_call("Starting JohMilAnt_Nackademin application")
        mock_logger.info.assert_any_call("Application completed successfully")


if __name__ == '__main__':
    unittest.main()