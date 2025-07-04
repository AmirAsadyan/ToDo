# 📝 ToDo App

A simple ToDo application built with Python.

## 📦 Features

- Add tasks
- Mark tasks as completed
- Remove tasks
- Load and save tasks to a CSV file
- Import task from CSV file

## 📁 Project Structure

```
todo_app/
│
├── app.py          # Main application runner
├── logic.py        # Core logic and helper functions
└── __init__.py     # Package marker

setup.py            # Installation script
requirements.txt    # Python dependencies
tasks.csv           # Task data storage
```

1. (Optional) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

2. Install dependencies:

```bash
pip install .
```

## 🛠 Usage

Run the app using:

```bash
todo
```

Make sure the `tasks.csv` file exists in the root directory (it will be created automatically if not).

## 🗑️ Uninstall

For uninstall simply run :

```bash
pip uninstall todo_app
```

# ======================================================================================================

# اپلیکیشن مدیریت کارها (To-Do List)

این یک اپلیکیشن دسکتاپ ساده برای مدیریت کارهای روزانه است که با استفاده از کتابخانه `tkinter` در پایتون ساخته شده. کاربر می‌تواند کارها را اضافه، حذف، و وضعیت آن‌ها را به‌روزرسانی کند. این پروژه به صورت یک پکیج قابل نصب پایتون طراحی شده است.

---

## ✨ ویژگی‌ها

- **افزودن کار:** قابلیت افزودن کار جدید با نام، توضیحات و سه سطح اولویت (پایین، متوسط، بالا).
- **نمایش لیست کارها:** نمایش کارها در یک جدول خوانا با رنگ‌بندی بر اساس اولویت.
- **تغییر وضعیت کار:** با یک کلیک می‌توان وضعیت کار را بین "انجام شده" و "انجام نشده" تغییر داد.
- **حذف کارها:** قابلیت حذف یک یا چند کار به صورت همزمان.
- **ذخیره‌سازی:** کارها به صورت خودکار در یک فایل `tasks.csv` ذخیره می‌شوند.
- **پاکسازی خودکار:** کارهای انجام‌شده‌ای که بیش از ۲۴ ساعت از تکمیل آن‌ها گذشته باشد، به صورت خودکار حذف می‌شوند.
- **نصب آسان:** پروژه به صورت یک پکیج استاندارد پایتون آماده شده و با یک دستور ساده نصب می‌شود.

---

## 📂 ساختار پروژه

todo_project/
├── todo_app/
│ ├── init.py # فایل خالی برای شناساندن پکیج
│ ├── app.py # کدهای مربوط به رابط کاربری (GUI)
│ └── logic.py # منطق اصلی برنامه و مدیریت کارها
├── requirements.txt # در حال حاضر خالی است چون وابستگی خارجی نداریم
├── setup.py # فایل تنظیمات برای نصب پکیج
└── README.md # همین فایل راهنما

---

## 🚀 نصب و اجرا

برای نصب و اجرای این برنامه، مراحل زیر را دنبال کنید.

### ۱. پیش‌نیازها

- **پایتون ۳.۶ یا بالاتر** (`Python 3.6+`)
- `pip` (که معمولاً همراه پایتون نصب می‌شود)

### ۲. مراحل نصب

۱. ابتدا پروژه را از طریق گیت کلون کنید یا فایل‌های آن را دانلود کنید.

۲. ترمینال (یا Command Prompt) را در پوشه اصلی پروژه باز کنید.

۳. دستور زیر را برای نصب برنامه و تمام نیازمندی‌های آن اجرا کنید:

```bash
pip install .
```

این دستور به صورت خودکار پکیج را نصب کرده و دستور اجرایی آن را به سیستم شما اضافه می‌کند.

۳. اجرای برنامه
بعد از نصب موفق، کافی است دستور زیر را در هر جای ترمینال خود وارد کنید تا برنامه اجرا شود:

```bash
todo
```

🗑️ حذف برنامه
برای حذف کامل پکیج از روی سیستم خود، دستور زیر را اجرا کنید:

```bash
pip uninstall todo_app
```
