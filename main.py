#!/usr/bin/env python3
"""
Solana Airdrop Tool - Main Entry Point

This is the main entry point for the Solana Airdrop Tool application.
It initializes the GUI and starts the application.

Usage:
    python main.py

Author: BJ-dev0706
Version: 1.0.0
"""

import sys
from pathlib import Path

src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.gui.main_window import MainWindow
from src.utils.config import config_manager
from src.utils.logger import setup_logger


def main():
    """Main application entry point."""
    try:
        logger = setup_logger()
        logger.info("=" * 50)
        logger.info("Starting Solana Airdrop Tool")
        logger.info("=" * 50)
        
        config_manager.ensure_directories()
        
        app = MainWindow()
        app.run()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"An unexpected error occurred: {e}")
        print("Check the logs for more details.")
    finally:
        logger.info("Application shutting down")


if __name__ == "__main__":
    main() 