# setup.py

import os
from setuptools import setup, find_packages # type: ignore

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

try:
    with open("requirements.txt", "r", encoding="utf-8") as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    requirements = []

setup(
    name="todo_app",
    version="0.1.0",
    author="AmirAsadyan",
    author_email="asadyanamir@gmail.com",
    description="A simple To-Do list application with Tkinter.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # آدرس ریپازیتوری گیت‌هاب پروژه
    url="https://github.com/AmirAsadyan/ToDo",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.13"       
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Desktop Environment",
        "Topic :: Utilities",
    ],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "todo=todo_app.app:main",
        ],
    },
    python_requires=">=3.8",
)
