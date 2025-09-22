#!/usr/bin/env python3
"""
Main entry point for JohMilAnt_Nackademin project.

This module serves as the main entry point for the application.
"""

import sys
import logging
from typing import Optional
from src.modules.core import CoreApplication
from src.config.settings import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main() -> int:
    """
    Main function - entry point of the application.
    
    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    app: Optional[CoreApplication] = None
    
    try:
        logger.info("Starting JohMilAnt_Nackademin application")
        
        # Initialize core application
        app = CoreApplication()
        if not app.initialize():
            logger.error("Failed to initialize application")
            return 1
        
        # Demo functionality
        print("Hello, JohMilAnt_Nackademin!")
        print(f"Application: {config.get('app_name')} v{config.get('version')}")
        
        # Process some demo data
        demo_data = ["Welcome to the application", "Processing demo data"]
        for data in demo_data:
            processed = app.process_data(data, "demo")
            if processed:
                logger.debug(f"Successfully processed: {processed}")
        
        # Show application status
        status = app.get_status()
        print(f"Application Status: {status['data_entries']} data entries processed")
        
        logger.info("Application completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Application failed with error: {e}")
        return 1
    
    finally:
        # Cleanup
        if app:
            app.shutdown()


if __name__ == "__main__":
    # Run main function and exit with the returned code
    sys.exit(main())
