"""
Airdrop Manager - Core airdrop functionality.

This module handles the main airdrop operations including browser automation,
form submission, and retry logic.
"""

import logging
import random
import time
from threading import Thread
from typing import Callable, Optional

from DrissionPage import ChromiumPage, ChromiumOptions
from plyer import notification

from .cloudflare_bypasser import CloudflareBypasser
from .browser_utils import BrowserUtils


class AirdropManager:
    """Manages airdrop operations and browser automation."""
    
    def __init__(self):
        self.last_attempt_time = 0
        self.logger = logging.getLogger(__name__)
        self.browser_utils = BrowserUtils()
        
    def get_chromium_options(self, arguments: list) -> ChromiumOptions:
        """Configure and return Chromium options."""
        options = ChromiumOptions()
        for argument in arguments:
            options.set_argument(argument)
        return options
    
    def _human_type(self, element, text: str) -> None:
        """Simulate human typing by inputting text with random delays."""
        for char in text:
            element.input(char)
            time.sleep(random.uniform(0.05, 0.1))
    
    def perform_airdrop(self, wallet_address: str, progress_callback: Callable[[str], None], attempt: int) -> bool:
        """
        Perform the airdrop process with error handling and progress updates.
        
        Args:
            wallet_address: The Solana wallet address
            progress_callback: Function to call with progress updates
            attempt: Current attempt number
            
        Returns:
            bool: True if airdrop was successful, False otherwise
        """
        try:
            progress_callback(f"Status: Starting airdrop attempt {attempt}...")
            
            options = self.get_chromium_options(["-no-first-run"])
            url = "https://faucet.solana.com/"
            page = ChromiumPage(addr_or_opts=options)
            
            self.logger.info("Navigating to the Solana Faucet page.")
            page.get(url)
            
            notification.notify(
                title="Airdrop Tool",
                message="Navigated to Solana Faucet page.",
                timeout=3
            )
            
            if not self._interact_with_page(page, wallet_address):
                return False
            
            self.logger.info("Attempting to bypass Cloudflare protection...")
            cf_bypasser = CloudflareBypasser(page)
            cf_bypasser.bypass()
            
            progress_callback("Status: Submitted form. Waiting for response...")
            time.sleep(10)
            
            success = self._check_airdrop_result(page, progress_callback, attempt)
            self.last_attempt_time = time.time()
            
            return success
            
        except Exception as e:
            self.logger.error("Error during the airdrop process", exc_info=True)
            error_message = f"An error occurred: {str(e)}"
            progress_callback(f"Status: {error_message}")
            return False
        finally:
            try:
                page.quit()
            except:
                pass
    
    def _interact_with_page(self, page: ChromiumPage, wallet_address: str) -> bool:
        """Handle page interactions for the airdrop form."""
        try:
            submit_button = page.ele('xpath://*[@type="button"]')
            if not submit_button:
                raise ValueError("Submit button not found.")
            submit_button.click()
            time.sleep(0.2)
            
            price_button = page.ele('xpath://*[@type="button" and text()="5"]')
            if not price_button:
                raise ValueError("Price button not found.")
            price_button.click()
            
            wallet_input = page.ele('xpath://*[@placeholder="Wallet Address"]')
            if not wallet_input:
                raise ValueError("Wallet input field not found.")
            wallet_input.click()
            time.sleep(0.1)
            
            self._human_type(wallet_input, wallet_address)
            time.sleep(0.2)
            
            submit_button = page.ele('xpath://*[@type="submit"]')
            if not submit_button:
                raise ValueError("Submit button not found during submission.")
            submit_button.click()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error interacting with page: {e}")
            return False
    
    def _check_airdrop_result(self, page: ChromiumPage, progress_callback: Callable[[str], None], attempt: int) -> bool:
        """Check the result of the airdrop attempt."""
        notification_element = None
        for _ in range(10):
            notification_element = page.ele('xpath:/html/body/section/main/form/div/ol/li/div')
            if notification_element:
                break
            time.sleep(2)
        
        if notification_element:
            message = notification_element.text
        else:
            message = "Notification not found. Check manually."
        
        progress_callback(f"Status: {message}")
        self.logger.info(f"Attempt {attempt} completed: {message}")
        
        return "success" in message.lower()
    
    def perform_airdrop_attempts(self, wallet_address: str, progress_callback: Callable[[str], None]) -> None:
        """
        Attempt the airdrop continuously with proper timing.
        
        Args:
            wallet_address: The Solana wallet address
            progress_callback: Function to call with progress updates
        """
        attempt = 1
        
        while True:
            time_since_last_attempt = time.time() - self.last_attempt_time
            if time_since_last_attempt < 3600:  # 1 hour cooldown
                wait_minutes = int((3600 - time_since_last_attempt) / 60)
                progress_callback(f"Status: Too soon to retry. Wait {wait_minutes} minutes.")
                self.logger.info(f"Waiting for {wait_minutes} minutes before retrying.")
                time.sleep(3600 - time_since_last_attempt)
            
            success = self.perform_airdrop(wallet_address, progress_callback, attempt)
            
            if success:
                progress_callback(f"Status: Attempt {attempt} successful. Retrying...")
                attempt += 1
                self.logger.info(f"Attempt {attempt} successful, proceeding to next attempt.")
                time.sleep(3)
            else:
                progress_callback(f"Status: Attempt {attempt} failed. Retrying after an hour.")
                self.logger.info(f"Attempt {attempt} failed, retrying after an hour.")
                time.sleep(3600)