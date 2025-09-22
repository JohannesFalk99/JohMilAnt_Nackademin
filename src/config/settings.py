"""
Configuration management for JohMilAnt_Nackademin.
"""

import os
from typing import Any, Dict


class Config:
    """Configuration class for application settings."""
    
    def __init__(self) -> None:
        """Initialize configuration with default values."""
        self.settings: Dict[str, Any] = {
            'debug': os.getenv('DEBUG', 'False').lower() == 'true',
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'app_name': 'JohMilAnt_Nackademin',
            'version': '0.1.0'
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self.settings[key] = value


# Global configuration instance
config = Config()