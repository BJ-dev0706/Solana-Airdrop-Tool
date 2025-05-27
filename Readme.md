# 🌟 Solana Airdrop Tool

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)](https://github.com/BJ-dev0706/solana-airdrop-tool)

An automated Python application designed to interact with Solana faucets, featuring Cloudflare bypass capabilities and a modern GUI interface.

## ✨ Features

- **🚀 Automated Airdrop Requests**: Seamlessly automates interaction with the Solana Faucet
- **🛡️ Cloudflare Bypass**: Advanced bypass mechanism for Cloudflare protection
- **⌨️ Human-like Typing**: Mimics natural typing patterns for enhanced authenticity
- **🔄 Smart Retry Logic**: Intelligent failure handling with automatic retries
- **📱 Real-time Updates**: Live status updates in GUI with desktop notifications
- **📝 Comprehensive Logging**: Detailed logging system for debugging and monitoring
- **🎨 Modern UI**: Clean, dark-themed interface with intuitive controls

## 📋 Prerequisites

- **Python 3.7+** installed on your system
- **Chrome/Chromium browser** (for DrissionPage automation)
- **Windows/Linux/macOS** (cross-platform support)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/BJ-dev0706/solana-airdrop-tool.git
cd solana-airdrop-tool
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python main.py
```

## 📁 Project Structure

```
solana-airdrop-tool/
├── src/                          # Source code
│   ├── __init__.py              # Package initialization
│   ├── core/                    # Core business logic
│   │   ├── __init__.py
│   │   ├── airdrop_manager.py   # Main airdrop functionality
│   │   ├── cloudflare_bypasser.py # Cloudflare bypass logic
│   │   └── browser_utils.py     # Browser automation utilities
│   ├── gui/                     # User interface
│   │   ├── __init__.py
│   │   └── main_window.py       # Main application window
│   └── utils/                   # Utility modules
│       ├── __init__.py
│       ├── logger.py            # Logging configuration
│       └── config.py            # Configuration management
├── assets/                      # Static assets
│   └── icon.ico                # Application icon
├── logs/                        # Log files (auto-created)
├── tests/                       # Unit tests
│   ├── __init__.py
│   └── test_browser_utils.py    # Sample test file
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup configuration
├── pyproject.toml              # Modern Python project config
├── Makefile                     # Development automation
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT License
└── README.md                    # Project documentation
```

## 🔧 Configuration

The application supports environment variable configuration:

```bash
# Browser settings
export BROWSER_TIMEOUT=30

# Retry settings
export RETRY_COOLDOWN=3600

# Logging level
export LOG_LEVEL=INFO

# Custom faucet URL
export FAUCET_URL=https://faucet.solana.com/
```

## 📖 Usage

1. **Launch the Application**: Run `python main.py`
2. **Enter Wallet Address**: Input your Solana wallet address (32-44 characters)
3. **Start Airdrop**: Click "🚀 Start Airdrop" to begin the process
4. **Monitor Progress**: Watch real-time status updates in the GUI
5. **Stop if Needed**: Use "⏹ Stop" button to halt the process

### Wallet Address Validation

The tool validates Solana wallet addresses using:
- Length check (32-44 characters)
- Base58 character validation
- Format verification

## 🔍 Logging

Logs are automatically saved to the `logs/` directory with:
- **File Logging**: Detailed logs with timestamps and function names
- **Console Logging**: Simplified output for real-time monitoring
- **Daily Rotation**: New log files created daily

## 🛠️ Development

### Setting up Development Environment

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Code formatting
black src/

# Linting
flake8 src/

# Type checking
mypy src/
```

### Using Makefile Commands

```bash
# Show all available commands
make help

# Install dependencies
make install

# Install development dependencies
make install-dev

# Run tests with coverage
make test

# Run linting checks
make lint

# Format code
make format

# Clean build artifacts
make clean

# Run the application
make run

# Build the package
make build
```

### Architecture Overview

- **Core Module**: Contains business logic for airdrop operations
- **GUI Module**: Handles user interface and event management
- **Utils Module**: Provides logging, configuration, and helper functions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational purposes only. Users are responsible for complying with the terms of service of any faucets they interact with. Use responsibly and respect rate limits.

## 🙏 Acknowledgments

- **DrissionPage**: For excellent browser automation capabilities
- **Plyer**: For cross-platform desktop notifications
- **Tkinter**: For the GUI framework

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/BJ-dev0706/solana-airdrop-tool/issues) page
2. Review the logs in the `logs/` directory
3. Create a new issue with detailed information

---

**Made with ❤️ by BJ-dev0706** 