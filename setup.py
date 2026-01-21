#!/usr/bin/env python3
"""
Setup script for KnowledgeSync.

This allows pip installation:
    pip install -e .
    
After installation:
    knowledgesync --help
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="knowledgesync",
    version="1.0.0",
    author="Forge (Team Brain)",
    author_email="logan@metaphy.llc",
    description="Cross-Agent Knowledge Synchronization for Team Brain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DonkRonk17/KnowledgeSync",
    py_modules=["knowledgesync"],
    python_requires=">=3.7",
    install_requires=[],  # Zero dependencies!
    entry_points={
        "console_scripts": [
            "knowledgesync=knowledgesync:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
    ],
    keywords="ai agents knowledge sync team-brain automation",
    project_urls={
        "Documentation": "https://github.com/DonkRonk17/KnowledgeSync#readme",
        "Source": "https://github.com/DonkRonk17/KnowledgeSync",
        "Issues": "https://github.com/DonkRonk17/KnowledgeSync/issues",
    },
)
