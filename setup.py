"""
Anahtar Üretici Deney Kurulum Scripti
"""

from setuptools import setup, find_packages
from pathlib import Path

# README dosyası
README = (Path(__file__).parent / "README.md").read_text(encoding='utf-8') if (Path(__file__).parent / "README.md").exists() else ""

# Requirements
REQUIREMENTS = [
    'pandas>=2.0.0',
    'numpy>=1.24.0', 
    'pathlib2>=2.3.7',
    'tqdm>=4.65.0',
    'colorama>=0.4.6'
]

setup(
    name="key-generator-experiment",
    version="1.0.0",
    description="Anahtar Üretici Deneysel Pipeline",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Research Team",
    author_email="research@example.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
        "Topic :: Scientific/Engineering",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "key-experiment=main:main",
        ]
    },
    python_requires=">=3.8",
)