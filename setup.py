# setup.py

import sys
from cx_Freeze import setup, Executable

# --- اطلاعات پایه برنامه ---
APP_NAME = "ToDo App"
VERSION = "2.0"
AUTHOR = "AmirAsadyan"
AUTHOR_EMAIL = "asadyanamir@gmail.com"
DESCRIPTION = "A simple and modern To-Do list application with Tkinter."

# خواندن توضیحات بلند از فایل README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# --- تنظیمات اصلی cx_Freeze ---

# فایل اجرایی اصلی برنامه (تغییر یافته به run.py)
executables = [
    Executable(
        "run.py",  # <--- نقطه شروع برنامه
        base="Win32GUI",
        target_name="todo.exe",
        icon="todo_app/icons/app_icon.ico",
    )
]

# فایل‌ها و پکیج‌هایی که باید در نصب‌کننده گنجانده شوند
included_files = ["todo_app/icons/"]
included_packages = [
    "tkinter",
    "tksvg",
    "todo_app",
]  # <-- پکیج اپلیکیشن خودت رو هم اضافه کن

# تنظیمات مربوط به ساخت فایل اجرایی
build_exe_options = {
    "packages": included_packages,
    "include_files": included_files,
    "include_msvcr": True,
}

# --- تنظیمات ساخت نصب‌کننده MSI ---

# تعریف میانبر دسکتاپ
shortcut_table = [
    (
        "DesktopShortcut",
        "DesktopFolder",
        APP_NAME,
        "TARGETDIR",
        "[TARGETDIR]todo.exe",
        None,
        None,
        None,
        None,
        None,
        None,
        "TARGETDIR",
    )
]

# تنظیمات نهایی MSI
bdist_msi_options = {
    "all_users": True,
    "data": {"Shortcut": shortcut_table},
    # این کد رو حتماً با کد GUID خودت جایگزین کن!
    "upgrade_code": "{9d254152-fe4a-4ed7-86cf-88ddf497b0d4}",  # <-- مثال
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\%s\%s" % (AUTHOR, APP_NAME),
}

# --- تابع اصلی setup ---

setup(
    name=APP_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AmirAsadyan/ToDo",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=executables,
)
