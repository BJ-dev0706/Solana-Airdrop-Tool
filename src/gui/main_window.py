"""
Main Window - Primary GUI interface for the Solana Airdrop Tool.

This module contains the main application window with all UI components
and event handlers.
"""

import tkinter as tk
from threading import Thread
from typing import Optional

from ..core.airdrop_manager import AirdropManager
from ..core.browser_utils import BrowserUtils
from ..utils.logger import setup_logger


class MainWindow:
    """Main application window for the Solana Airdrop Tool."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.airdrop_manager = AirdropManager()
        self.browser_utils = BrowserUtils()
        self.logger = setup_logger()
        
        self.wallet_entry: Optional[tk.Entry] = None
        self.progress_label: Optional[tk.Label] = None
        self.confirm_button: Optional[tk.Button] = None
        self.stop_button: Optional[tk.Button] = None
        
        self.is_running = False
        self.current_thread: Optional[Thread] = None
        
        self._setup_window()
        self._create_widgets()
        
    def _setup_window(self) -> None:
        """Configure the main window properties."""
        self.root.title("🌟 Solana Airdrop Tool 🌟")
        self.root.geometry("450x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a1a")
        
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"450x500+{x}+{y}")
        
    def _create_widgets(self) -> None:
        """Create and arrange all UI widgets."""
        self._create_title_section()
        
        self._create_input_section()
        
        self._create_control_section()
        
        self._create_status_section()
        
        self._create_footer_section()
        
    def _create_title_section(self) -> None:
        """Create the title section with app branding."""
        title_frame = tk.Frame(self.root, bg="#1a1a1a")
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🌟 Solana Airdrop Tool 🌟",
            font=("Helvetica", 18, "bold"),
            bg="#1a1a1a",
            fg="#00d4ff"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Automated Solana Faucet Interaction",
            font=("Helvetica", 10),
            bg="#1a1a1a",
            fg="#888888"
        )
        subtitle_label.pack(pady=(5, 0))
        
    def _create_input_section(self) -> None:
        """Create the wallet address input section."""
        input_frame = tk.Frame(self.root, bg="#2a2a2a", relief="raised", bd=1)
        input_frame.pack(pady=20, padx=30, fill="x")
        
        inner_frame = tk.Frame(input_frame, bg="#2a2a2a")
        inner_frame.pack(padx=20, pady=20)
        
        wallet_label = tk.Label(
            inner_frame,
            text="Solana Wallet Address:",
            font=("Helvetica", 12, "bold"),
            bg="#2a2a2a",
            fg="#ffffff"
        )
        wallet_label.pack(anchor="w", pady=(0, 8))
        
        self.wallet_entry = tk.Entry(
            inner_frame,
            width=40,
            font=("Consolas", 11),
            relief="flat",
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000"
        )
        self.wallet_entry.pack(pady=(0, 10), ipady=8)
        
        hint_label = tk.Label(
            inner_frame,
            text="Enter a valid Solana wallet address (32-44 characters)",
            font=("Helvetica", 9),
            bg="#2a2a2a",
            fg="#888888"
        )
        hint_label.pack(anchor="w")
        
    def _create_control_section(self) -> None:
        """Create the control buttons section."""
        control_frame = tk.Frame(self.root, bg="#1a1a1a")
        control_frame.pack(pady=20)
        
        self.confirm_button = tk.Button(
            control_frame,
            text="🚀 Start Airdrop",
            font=("Helvetica", 12, "bold"),
            bg="#00d4ff",
            fg="#000000",
            relief="flat",
            command=self._on_confirm,
            width=15,
            height=2
        )
        self.confirm_button.pack(side="left", padx=10)
        
        self.stop_button = tk.Button(
            control_frame,
            text="⏹ Stop",
            font=("Helvetica", 12, "bold"),
            bg="#ff4444",
            fg="#ffffff",
            relief="flat",
            command=self._on_stop,
            width=15,
            height=2,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=10)
        
    def _create_status_section(self) -> None:
        """Create the status display section."""
        status_frame = tk.Frame(self.root, bg="#2a2a2a", relief="sunken", bd=1)
        status_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        status_title = tk.Label(
            status_frame,
            text="Status",
            font=("Helvetica", 12, "bold"),
            bg="#2a2a2a",
            fg="#ffffff"
        )
        status_title.pack(pady=(10, 5))
        
        self.progress_label = tk.Label(
            status_frame,
            text="Ready to start. Enter your wallet address and click 'Start Airdrop'.",
            font=("Helvetica", 10),
            bg="#2a2a2a",
            fg="#00ff88",
            wraplength=350,
            justify="center"
        )
        self.progress_label.pack(pady=10, padx=20)
        
    def _create_footer_section(self) -> None:
        """Create the footer section."""
        footer_frame = tk.Frame(self.root, bg="#1a1a1a")
        footer_frame.pack(side="bottom", pady=10)
        
        footer_label = tk.Label(
            footer_frame,
            text="© Powered by BJ-dev0706",
            font=("Helvetica", 9),
            bg="#1a1a1a",
            fg="#666666"
        )
        footer_label.pack()
        
    def _update_progress(self, message: str) -> None:
        """
        Update the progress label with a new message.
        
        Args:
            message: Status message to display
        """
        if self.progress_label:
            self.progress_label.config(text=message)
            
            if "error" in message.lower() or "failed" in message.lower():
                self.progress_label.config(fg="#ff4444")
            elif "successful" in message.lower() or "success" in message.lower():
                self.progress_label.config(fg="#00ff88")
            elif "waiting" in message.lower() or "retry" in message.lower():
                self.progress_label.config(fg="#ffaa00")
            else:
                self.progress_label.config(fg="#00d4ff")
                
    def _on_confirm(self) -> None:
        """Handle the confirm button click event."""
        if self.is_running:
            return
            
        wallet_address = self.wallet_entry.get().strip()
        
        if not wallet_address:
            self._update_progress("Error: Please enter a wallet address.")
            return
            
        if not self.browser_utils.validate_wallet_address(wallet_address):
            self._update_progress("Error: Invalid wallet address format.")
            return
            
        self.is_running = True
        self.confirm_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.wallet_entry.config(state="disabled")
        
        self._update_progress("Starting airdrop process...")
        
        self.current_thread = Thread(
            target=self.airdrop_manager.perform_airdrop_attempts,
            args=(wallet_address, self._update_progress),
            daemon=True
        )
        self.current_thread.start()
        
    def _on_stop(self) -> None:
        """Handle the stop button click event."""
        if not self.is_running:
            return
            
        self.is_running = False
        self.confirm_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.wallet_entry.config(state="normal")
        
        self._update_progress("Stopped by user. Ready to start again.")
        
    def run(self) -> None:
        """Start the GUI application."""
        self.logger.info("Starting Solana Airdrop Tool GUI")
        self.root.mainloop()
        
    def destroy(self) -> None:
        """Clean up and destroy the window."""
        self.is_running = False
        self.root.destroy() 