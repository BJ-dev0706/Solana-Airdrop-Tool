import tkinter as tk
from plyer import notification
from DrissionPage import ChromiumPage, ChromiumOptions
from CloudflareBypasser import CloudflareBypasser
import logging
from time import sleep
import random
from threading import Thread
import time  # For timestamp tracking

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("airdrop_tool.log"), logging.StreamHandler()]
)

# Global variable to track the time of the last attempt
last_attempt_time = 0  # Initialize with 0 (no attempts yet)

def get_chromium_options(arguments: list) -> ChromiumOptions:
    """Configure and return Chromium options."""
    options = ChromiumOptions()
    for argument in arguments:
        options.set_argument(argument)
    return options


def _human_type(element, text: str) -> None:
    """Simulate human typing by inputting text with random delays."""
    for char in text:
        element.input(char)
        sleep(random.uniform(0.05, 0.1))


def perform_airdrop(wallet_address: str, progress_label, attempt: int) -> None:
    """Perform the airdrop process with error handling and UI updates."""
    global last_attempt_time

    try:
        # Update progress label in the UI thread
        progress_label.config(text=f"Status: Starting airdrop attempt {attempt}...")

        # Set up Chromium options
        options = get_chromium_options(["-no-first-run"])
        url = "https://faucet.solana.com/"
        page = ChromiumPage(addr_or_opts=options)

        logging.info("Navigating to the Solana Faucet page.")
        page.get(url)

        # Send notification for page navigation
        notification.notify(
            title="Airdrop Tool",
            message="Navigated to Solana Faucet page.",
            timeout=3
        )

        # Interact with the page elements
        submit_button = page.ele('xpath://*[@type="button"]')
        if not submit_button:
            raise ValueError("Submit button not found.")
        submit_button.click()
        sleep(0.2)

        price_button = page.ele('xpath://*[@type="button" and text()="5"]')
        if not price_button:
            raise ValueError("Price button not found.")
        price_button.click()

        wallet_input = page.ele('xpath://*[@placeholder="Wallet Address"]')
        if not wallet_input:
            raise ValueError("Wallet input field not found.")
        wallet_input.click()
        sleep(0.1)

        _human_type(wallet_input, wallet_address)
        sleep(0.2)

        submit_button = page.ele('xpath://*[@type="submit"]')
        if not submit_button:
            raise ValueError("Submit button not found during submission.")
        submit_button.click()

        # Bypass Cloudflare
        logging.info("Attempting to bypass Cloudflare protection...")
        cf_bypasser = CloudflareBypasser(page)
        cf_bypasser.bypass()

        # Update progress and wait for the response
        progress_label.config(text="Status: Submitted form. Waiting for response...")
        sleep(10)

        # Fetch response notification with retry mechanism
        notification_element = None
        for _ in range(10):  # Try up to 10 times with a delay
            notification_element = page.ele('xpath:/html/body/section/main/form/div/ol/li/div')
            if notification_element:
                break
            sleep(2)  # Wait 2 seconds before checking again

        # Determine message from notification
        if notification_element:
            message = notification_element.text
        else:
            message = "Notification not found. Check manually."

        progress_label.config(text=f"Status: {message}")
        logging.info(f"Attempt {attempt} completed: {message}")

        # Check if the airdrop was successful based on the message
        if "success" in message.lower():
            last_attempt_time = time.time()  # Update the timestamp after successful attempt
            return True  # Airdrop was successful
        else:
            last_attempt_time = time.time()  # Update the timestamp after failure
            return False  # Airdrop failed

    except Exception as e:
        logging.error("Error during the airdrop process", exc_info=True)
        error_message = f"An error occurred: {str(e)}"
        progress_label.config(text=f"Status: {error_message}")
        return False


def on_confirm():
    """Handle Confirm button click to initiate the airdrop."""
    wallet_address = wallet_entry.get().strip()
    if wallet_address:
        progress_label.config(text="Status: Processing...")
        Thread(target=perform_airdrop_attempts, args=(wallet_address, progress_label), daemon=True).start()
    else:
        progress_label.config(text="Status: Please enter a valid wallet address.")


def perform_airdrop_attempts(wallet_address: str, progress_label) -> None:
    """Attempt the airdrop continuously until manually stopped or if it fails."""
    global last_attempt_time
    attempt = 1

    while True:
        # Ensure we are waiting the necessary time before retrying
        time_since_last_attempt = time.time() - last_attempt_time
        if time_since_last_attempt < 3600:  # Retry if less than 1 hour has passed
            progress_label.config(text=f"Status: Too soon to retry. Wait {int((3600 - time_since_last_attempt) / 60)} minutes.")
            logging.info(f"Waiting for {int((3600 - time_since_last_attempt) / 60)} minutes before retrying.")
            sleep(3600 - time_since_last_attempt)  # Wait until an hour has passed

        success = perform_airdrop(wallet_address, progress_label, attempt)
        if success:
            progress_label.config(text=f"Status: Attempt {attempt} successful. Retrying...")
            attempt += 1
            logging.info(f"Attempt {attempt} successful, proceeding to next attempt.")
            sleep(3)  # Wait for 30 minutes before trying again after success
        else:
            progress_label.config(text=f"Status: Attempt {attempt} failed. Retrying after an hour.")
            attempt = 0
            logging.info(f"Attempt {attempt} failed, retrying after an hour.")
            sleep(3600)  # Wait for an hour before retrying

# Create main application window
root = tk.Tk()
root.title("Solana Airdrop Tool")
root.geometry("400x400")
root.resizable(False, False)
root.configure(bg="#1c1c1c")

# Title Label
title_label = tk.Label(
    root,
    text="🌟 Solana Airdrop 🌟",
    font=("Helvetica", 16, "bold"),
    bg="#1c1c1c",
    fg="#ffffff"
)
title_label.pack(pady=10)

# Frame for input
input_frame = tk.Frame(root, bg="#2c2c2c", padx=20, pady=20)
input_frame.pack(pady=30)

# Wallet Address Label
wallet_label = tk.Label(
    input_frame,
    text="Enter Wallet Address:",
    font=("Helvetica", 12),
    bg="#2c2c2c",
    fg="#ffffff"
)
wallet_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

# Wallet Address Entry
wallet_entry = tk.Entry(
    input_frame,
    width=30,
    font=("Helvetica", 12),
    relief="flat",
    bg="#ffffff",
    fg="#000000"
)
wallet_entry.grid(row=1, column=0, pady=(0, 10))

# Confirm Button
confirm_button = tk.Button(
    input_frame,
    text="Confirm",
    font=("Helvetica", 12, "bold"),
    bg="#4caf50",
    fg="#ffffff",
    relief="flat",
    command=on_confirm
)
confirm_button.grid(row=2, column=0, pady=10)

# Progress Label
progress_label = tk.Label(
    root,
    text="Status: Waiting for input...",
    font=("Helvetica", 10),
    bg="#1c1c1c",
    fg="#ffffff"
)
progress_label.pack(side="bottom", pady=10)

# Footer Label
footer_label = tk.Label(
    root,
    text="@ Powered by Alibaba @",
    font=("Helvetica", 10),
    bg="#1c1c1c",
    fg="#ffffff"
)
footer_label.pack(side="bottom", pady=10)

# Start the application
root.mainloop()

