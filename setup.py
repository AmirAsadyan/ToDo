import os
from setuptools import setup, find_packages  # type: ignore

# خواندن پیش‌نیازها از فایل requirements.txt
try:
    with open("requirements.txt", "r", encoding="utf-8") as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    requirements = []

setup(
    name="todo_app",
    version="0.1.0",
    author="AmirAsadyan",
    description="A simple To-Do list application with Tkinter.",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GUN General Public License v2.0",
    ],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            # مسیر جدید به تابع main را مشخص می‌کنیم
            "todo=todo_app.app:main",
        ],
    },
    python_requires=">=3.6",
)
