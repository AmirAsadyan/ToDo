# logic.py

import csv
import os
from datetime import datetime, timedelta


class Task:
    """کلاسی برای مدل‌سازی یک کار تکی با وضعیت و تاریخ انجام."""

    def __init__(
        self, name, description, priority, status="انجام نشده", completion_date=None
    ):
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status
        # تاریخ انجام کار را به صورت رشته ذخیره می‌کنیم
        self.completion_date = completion_date

    def to_list(self):
        """یک کار را برای نوشتن در فایل CSV به لیست تبدیل می‌کند."""
        return [
            self.name,
            self.description,
            self.priority,
            self.status,
            self.completion_date or "",
        ]


class ToDoList:
    """کلاسی برای مدیریت کل لیست کارها و فایل CSV."""

    def __init__(self, filename="tasks.csv"):
        self.filename = filename
        self.tasks = []
        self._load_tasks()
        # در ابتدای اجرای برنامه، کارهای قدیمی را پاک کن
        self._cleanup_old_tasks()

    def _load_tasks(self):
        """کارها را از فایل CSV اصلی برنامه بارگذاری می‌کند."""
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader, None)
                for row in reader:
                    if len(row) == 5:  # برای سازگاری با فایل‌های جدید
                        # اگر تاریخ خالی بود، None را جایگزین کن
                        completion_date = row[4] if row[4] else None
                        self.tasks.append(
                            Task(
                                name=row[0],
                                description=row[1],
                                priority=row[2],
                                status=row[3],
                                completion_date=completion_date,
                            )
                        )
                    elif len(row) == 4:  # برای سازگاری با فایل‌های قدیمی‌تر
                        self.tasks.append(
                            Task(
                                name=row[0],
                                description=row[1],
                                priority=row[2],
                                status=row[3],
                            )
                        )
        except Exception as e:
            print(f"خطا در بارگذاری فایل: {e}")

    def _save_tasks(self):
        """کل لیست کارها را در فایل CSV اصلی برنامه ذخیره می‌کند."""
        try:
            with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["Name", "Description", "Priority", "Status", "CompletionDate"]
                )
                for task in self.tasks:
                    writer.writerow(task.to_list())
        except Exception as e:
            print(f"خطا در ذخیره فایل: {e}")

    def _cleanup_old_tasks(self):
        """کارهای انجام شده‌ای که بیش از ۲۴ ساعت از انجامشان گذشته را حذف می‌کند."""
        now = datetime.now()
        tasks_to_keep = []
        tasks_were_deleted = False

        for task in self.tasks:
            # فقط کارهایی که انجام شده و تاریخ انجام دارند را بررسی کن
            if task.status == "انجام شده" and task.completion_date:
                try:
                    completion_time = datetime.fromisoformat(task.completion_date)
                    # اگر بیشتر از ۲۴ ساعت گذشته بود، آن را به لیست جدید اضافه نکن
                    if now - completion_time > timedelta(hours=24):
                        tasks_were_deleted = True
                        continue  # این کار حذف می‌شود
                except (ValueError, TypeError):
                    pass  # اگر تاریخ فرمت درستی نداشت، نادیده بگیر

            tasks_to_keep.append(task)

        # اگر کاری حذف شده بود، لیست اصلی را به‌روز کرده و فایل را ذخیره کن
        if tasks_were_deleted:
            self.tasks = tasks_to_keep
            self._save_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self._save_tasks()

    def delete_multiple_tasks(self, indices):
        for index in sorted(indices, reverse=True):
            if 0 <= index < len(self.tasks):
                del self.tasks[index]
        self._save_tasks()

    def toggle_task_status(self, task_index):
        """وضعیت یک کار را تغییر داده و تاریخ انجام را ثبت یا حذف می‌کند."""
        if 0 <= task_index < len(self.tasks):
            task = self.tasks[task_index]
            if task.status == "انجام نشده":
                task.status = "انجام شده"
                # زمان فعلی را به صورت رشته استاندارد ذخیره کن
                task.completion_date = datetime.now().isoformat()
            else:
                task.status = "انجام نشده"
                task.completion_date = None  # تاریخ را پاک کن
            self._save_tasks()

    def import_from_csv(self, filepath):
        try:
            with open(filepath, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader, None)
                required_header = [
                    "Name",
                    "Description",
                    "Priority",
                    "Status",
                    "CompletionDate",
                ]
                if header != required_header:
                    return False, f"فایل CSV باید شامل ستون‌های {required_header} باشد."
                for row in reader:
                    if row:
                        completion_date = row[4] if row[4] else None
                        self.tasks.append(
                            Task(
                                name=row[0],
                                description=row[1],
                                priority=row[2],
                                status=row[3],
                                completion_date=completion_date,
                            )
                        )
            self._save_tasks()
            return True, "کارها با موفقیت از فایل CSV اضافه شدند."
        except Exception as e:
            return False, f"خطا در پردازش فایل CSV: {e}"
