"""
Tests for browser utilities module.
"""

import pytest
from src.core.browser_utils import BrowserUtils


class TestBrowserUtils:
    """Test cases for BrowserUtils class."""
    
    def test_validate_wallet_address_valid(self):
        """Test wallet address validation with valid addresses."""
        valid_addresses = [
            "11111111111111111111111111111111",
            "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
            "DjVE6JNiYqPL2QXyCUUh8rNjHrbz9hXHNYt99MQ59qw1",
        ]
        
        for address in valid_addresses:
            assert BrowserUtils.validate_wallet_address(address) is True
    
    def test_validate_wallet_address_invalid(self):
        """Test wallet address validation with invalid addresses."""
        invalid_addresses = [
            "",
            "short",
            "0" * 50,
            "InvalidChars!@#$%^&*()",
            None,
        ]
        
        for address in invalid_addresses:
            assert BrowserUtils.validate_wallet_address(address) is False 