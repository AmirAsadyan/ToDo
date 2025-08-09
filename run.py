# run.py

from todo_app import app

# این فایل به عنوان یک راه‌انداز عمل می‌کند تا مشکل ایمپورت‌های نسبی
# در زمان پکیج کردن با cx_Freeze حل شود.
if __name__ == "__main__":
    app.main()
