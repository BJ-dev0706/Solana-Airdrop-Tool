"""
Browser Utilities - Common browser automation utilities.

This module provides utility functions for browser automation,
including element interaction and validation.
"""

import random
import time
from typing import Optional

from DrissionPage import ChromiumPage


class BrowserUtils:
    """Utility class for browser automation tasks."""
    
    @staticmethod
    def human_type(element, text: str, min_delay: float = 0.05, max_delay: float = 0.1) -> None:
        """
        Simulate human typing by inputting text with random delays.
        
        Args:
            element: The input element to type into
            text: Text to type
            min_delay: Minimum delay between keystrokes
            max_delay: Maximum delay between keystrokes
        """
        for char in text:
            element.input(char)
            time.sleep(random.uniform(min_delay, max_delay))
    
    @staticmethod
    def wait_for_element(page: ChromiumPage, xpath: str, timeout: int = 10) -> Optional[object]:
        """
        Wait for an element to appear on the page.
        
        Args:
            page: ChromiumPage instance
            xpath: XPath selector for the element
            timeout: Maximum time to wait in seconds
            
        Returns:
            Element if found, None otherwise
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            element = page.ele(f'xpath:{xpath}')
            if element:
                return element
            time.sleep(0.5)
        return None
    
    @staticmethod
    def safe_click(element, delay: float = 0.1) -> bool:
        """
        Safely click an element with error handling.
        
        Args:
            element: Element to click
            delay: Delay after clicking
            
        Returns:
            True if successful, False otherwise
        """
        try:
            element.click()
            time.sleep(delay)
            return True
        except Exception:
            return False
    
    @staticmethod
    def validate_wallet_address(address: str) -> bool:
        """
        Validate a Solana wallet address format.
        
        Args:
            address: Wallet address to validate
            
        Returns:
            True if valid format, False otherwise
        """
        if not address:
            return False
        
        if len(address) < 32 or len(address) > 44:
            return False
        
        valid_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        return all(c in valid_chars for c in address) 