"""
Setup script for Solana Airdrop Tool.

This script allows the package to be installed using pip and provides
metadata about the project.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = requirements_path.read_text(encoding="utf-8").strip().split("\n")
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("#")]

setup(
    name="solana-airdrop-tool",
    version="1.0.0",
    author="BJ-dev0706",
    author_email="",
    description="Automated Solana Faucet Interaction Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BJ-dev0706/solana-airdrop-tool",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Office/Business :: Financial",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "solana-airdrop-tool=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.ico", "*.png", "*.jpg", "*.gif"],
    },
    keywords="solana, airdrop, faucet, automation, cryptocurrency, blockchain",
    project_urls={
        "Bug Reports": "https://github.com/BJ-dev0706/solana-airdrop-tool/issues",
        "Source": "https://github.com/BJ-dev0706/solana-airdrop-tool",
        "Documentation": "https://github.com/BJ-dev0706/solana-airdrop-tool/blob/main/README.md",
    },
) 