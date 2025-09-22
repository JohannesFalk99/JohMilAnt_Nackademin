"""
Core functionality for JohMilAnt_Nackademin.
"""

import logging
from typing import Any, Dict, List, Optional
from src.config.settings import config
from src.utils.helpers import setup_logger, validate_input, sanitize_string


class CoreApplication:
    """Core application class with basic functionality."""
    
    def __init__(self) -> None:
        """Initialize the core application."""
        self.logger = setup_logger(__name__, config.get('log_level', 'INFO'))
        self.is_initialized = False
        self.data_store: Dict[str, Any] = {}
        
    def initialize(self) -> bool:
        """
        Initialize the application.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing core application")
            
            # Add initialization logic here
            self.data_store = {}
            self.is_initialized = True
            
            self.logger.info("Core application initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize application: {e}")
            return False
    
    def process_data(self, data: Any, data_type: str = "generic") -> Optional[Any]:
        """
        Process input data with validation and sanitization.
        
        Args:
            data: Data to process
            data_type: Type of data being processed
            
        Returns:
            Processed data or None if processing failed
        """
        try:
            if not self.is_initialized:
                raise RuntimeError("Application not initialized")
            
            self.logger.debug(f"Processing {data_type} data")
            
            # Basic validation
            if data is None:
                raise ValueError("Data cannot be None")
            
            # If it's a string, sanitize it
            if isinstance(data, str):
                data = sanitize_string(data)
            
            # Store processed data
            timestamp_key = f"{data_type}_{len(self.data_store)}"
            self.data_store[timestamp_key] = data
            
            self.logger.debug(f"Data processed and stored with key: {timestamp_key}")
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to process data: {e}")
            return None
    
    def get_stored_data(self, key: Optional[str] = None) -> Any:
        """
        Retrieve stored data.
        
        Args:
            key: Specific key to retrieve, or None for all data
            
        Returns:
            Stored data or all data if key is None
        """
        if key is None:
            return self.data_store.copy()
        return self.data_store.get(key)
    
    def clear_data(self) -> None:
        """Clear all stored data."""
        self.logger.info("Clearing all stored data")
        self.data_store.clear()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get application status information.
        
        Returns:
            Dictionary containing status information
        """
        return {
            'initialized': self.is_initialized,
            'data_entries': len(self.data_store),
            'config': {
                'debug': config.get('debug'),
                'log_level': config.get('log_level'),
                'app_name': config.get('app_name'),
                'version': config.get('version')
            }
        }
    
    def shutdown(self) -> None:
        """Safely shutdown the application."""
        try:
            self.logger.info("Shutting down core application")
            self.clear_data()
            self.is_initialized = False
            self.logger.info("Core application shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")