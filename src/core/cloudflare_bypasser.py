"""
Cloudflare Bypasser - Handles Cloudflare protection bypass.

This module provides functionality to automatically bypass Cloudflare
verification challenges using browser automation.
"""

import time
from typing import Optional

from DrissionPage import ChromiumPage


class CloudflareBypasser:
    """Handles bypassing Cloudflare verification challenges."""
    
    def __init__(self, driver: ChromiumPage, max_retries: int = -1, log: bool = True):
        """
        Initialize the Cloudflare bypasser.
        
        Args:
            driver: ChromiumPage instance
            max_retries: Maximum number of retry attempts (-1 for unlimited)
            log: Whether to enable logging
        """
        self.driver = driver
        self.max_retries = max_retries
        self.log = log

    def search_recursively_shadow_root_with_iframe(self, ele) -> Optional[object]:
        """
        Recursively search for iframe in shadow root elements.
        
        Args:
            ele: Element to search in
            
        Returns:
            iframe element if found, None otherwise
        """
        if ele.shadow_root:
            if ele.shadow_root.child().tag == "iframe":
                return ele.shadow_root.child()
        else:
            for child in ele.children():
                result = self.search_recursively_shadow_root_with_iframe(child)
                if result:
                    return result
        return None

    def search_recursively_shadow_root_with_cf_input(self, ele) -> Optional[object]:
        """
        Recursively search for Cloudflare input in shadow root elements.
        
        Args:
            ele: Element to search in
            
        Returns:
            input element if found, None otherwise
        """
        if ele.shadow_root:
            if ele.shadow_root.ele("tag:input"):
                return ele.shadow_root.ele("tag:input")
        else:
            for child in ele.children():
                result = self.search_recursively_shadow_root_with_cf_input(child)
                if result:
                    return result
        return None
    
    def locate_cf_button(self) -> Optional[object]:
        """
        Locate the Cloudflare verification button.
        
        Returns:
            Button element if found, None otherwise
        """
        button = None
        eles = self.driver.eles("tag:input")
        
        for ele in eles:
            if "name" in ele.attrs.keys() and "type" in ele.attrs.keys():
                if "turnstile" in ele.attrs["name"] and ele.attrs["type"] == "hidden":
                    button = ele.parent().shadow_root.child()("tag:body").shadow_root("tag:input")
                    break
            
        if button:
            return button
        else:
            self.log_message("Basic search failed. Searching for button recursively.")
            ele = self.driver.ele("tag:body")
            iframe = self.search_recursively_shadow_root_with_iframe(ele)
            if iframe:
                button = self.search_recursively_shadow_root_with_cf_input(iframe("tag:body"))
            else:
                self.log_message("Iframe not found. Button search failed.")
            return button

    def log_message(self, message: str) -> None:
        """
        Log a message if logging is enabled.
        
        Args:
            message: Message to log
        """
        if self.log:
            print(f"[CloudflareBypasser] {message}")

    def click_verification_button(self) -> None:
        """Attempt to click the Cloudflare verification button."""
        try:
            button = self.locate_cf_button()
            if button:
                self.log_message("Verification button found. Attempting to click.")
                button.click()
            else:
                self.log_message("Verification button not found.")

        except Exception as e:
            self.log_message(f"Error clicking verification button: {e}")

    def is_bypassed(self) -> bool:
        """
        Check if Cloudflare protection has been bypassed.
        
        Returns:
            True if bypassed, False otherwise
        """
        try:
            title = self.driver.title.lower()
            return "just a moment" not in title
        except Exception as e:
            self.log_message(f"Error checking page title: {e}")
            return False

    def bypass(self) -> bool:
        """
        Attempt to bypass Cloudflare protection.
        
        Returns:
            True if successful, False otherwise
        """
        try_count = 0

        while not self.is_bypassed():
            if 0 < self.max_retries + 1 <= try_count:
                self.log_message("Exceeded maximum retries. Bypass failed.")
                return False

            self.log_message(f"Attempt {try_count + 1}: Verification page detected. Trying to bypass...")
            self.click_verification_button()

            try_count += 1
            time.sleep(2)

        if self.is_bypassed():
            self.log_message("Bypass successful.")
            return True
        else:
            self.log_message("Bypass failed.")
            return False 