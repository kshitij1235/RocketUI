from __future__ import annotations

from pathlib import Path

from setuptools import find_packages, setup

from project_config import VERSION

BASE_DIR = Path(__file__).parent

setup(
    name="Rocket",
    version=VERSION,
    description="Rocket UI Framework and CLI",
    long_description=(BASE_DIR / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Rocket",
    python_requires=">=3.10",
    packages=find_packages(
        exclude=("app", "resources", "build", "dist", "__pycache__")
    ),
    include_package_data=True,
    install_requires=[
        "click",
        "watchdog",
        "customtkinter",
    ],
    entry_points={
        "console_scripts": [
            "rocket=rocket.cli.main:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
