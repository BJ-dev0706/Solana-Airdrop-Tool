"""
Configuration Management - Application settings and constants.

This module contains configuration settings, constants, and environment
variable management for the application.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class AppConfig:
    """Application configuration settings."""
    
    app_name: str = "Solana Airdrop Tool"
    app_version: str = "2.0.1"
    app_author: str = "BJ-dev0706"
       
    solana_faucet_url: str = "https://faucet.solana.com/"
    
    browser_arguments: List[str] = None
    page_load_timeout: int = 30
    element_wait_timeout: int = 10
    
    retry_cooldown_seconds: int = 3600
    success_wait_seconds: int = 3
    typing_min_delay: float = 0.05
    typing_max_delay: float = 0.1
    
    window_width: int = 450
    window_height: int = 500
    window_resizable: bool = False
    
    log_level: str = "INFO"
    log_to_file: bool = True
    log_to_console: bool = True
    
    logs_dir: str = "logs"
    assets_dir: str = "assets"
    
    def __post_init__(self):
        """Initialize default values after dataclass creation."""
        if self.browser_arguments is None:
            self.browser_arguments = ["-no-first-run"]


class ConfigManager:
    """Manages application configuration and environment variables."""
    
    def __init__(self):
        self.config = AppConfig()
        self._load_from_env()
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        if os.getenv("BROWSER_TIMEOUT"):
            try:
                self.config.page_load_timeout = int(os.getenv("BROWSER_TIMEOUT"))
            except ValueError:
                pass
        
        if os.getenv("RETRY_COOLDOWN"):
            try:
                self.config.retry_cooldown_seconds = int(os.getenv("RETRY_COOLDOWN"))
            except ValueError:
                pass
        
        if os.getenv("LOG_LEVEL"):
            self.config.log_level = os.getenv("LOG_LEVEL").upper()
        
        if os.getenv("FAUCET_URL"):
            self.config.solana_faucet_url = os.getenv("FAUCET_URL")
    
    def get_config(self) -> AppConfig:
        """
        Get the current configuration.
        
        Returns:
            AppConfig instance
        """
        return self.config
    
    def get_logs_path(self) -> Path:
        """
        Get the logs directory path.
        
        Returns:
            Path to logs directory
        """
        return Path(self.config.logs_dir)
    
    def get_assets_path(self) -> Path:
        """
        Get the assets directory path.
        
        Returns:
            Path to assets directory
        """
        return Path(self.config.assets_dir)
    
    def ensure_directories(self) -> None:
        """Ensure required directories exist."""
        self.get_logs_path().mkdir(exist_ok=True)
        self.get_assets_path().mkdir(exist_ok=True)


config_manager = ConfigManager()
config = config_manager.get_config() 