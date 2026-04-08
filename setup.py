"""
Setup script for Adaptive Neuro-Symbolic Market Intelligence System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="adaptive-market-intelligence",
    version="1.0.0",
    author="Market Intelligence Team",
    author_email="team@marketintelligence.com",
    description="Adaptive Neuro-Symbolic Market Intelligence System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/adaptive-market-intelligence",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "gpu": [
            "torch-audio",
            "transformers[torch]",
            "tensorflow",
        ],
    },
    entry_points={
        "console_scripts": [
            "market-intelligence-api=backend.main:main",
            "market-intelligence-dashboard=dashboard.app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
)
