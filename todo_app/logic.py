# logic.py

import csv
import os
import base64
import time
import json
from datetime import datetime, timedelta


class Task:
    """کلاسی برای مدل‌سازی یک کار تکی با وضعیت و تاریخ انجام."""

    def __init__(
        self,
        name,
        description,
        priority,
        status="انجام نشده",
        completion_date=None,
        due_date=None,
        category=None,
        task_id=None,
        parent_id=None,
        subtask_order=None,
        is_recurring=False,
        recurrence_pattern=None,
        notes=""
    ):
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status
        self.completion_date = completion_date
        self.due_date = due_date
        self.category = category or "بدون دسته"
        self.task_id = task_id or self._generate_task_id()
        self.parent_id = parent_id
        self.subtask_order = subtask_order
        self.is_recurring = is_recurring
        self.recurrence_pattern = recurrence_pattern
        self.notes = notes
        self.subtasks = []

    def _generate_task_id(self):
        """تولید شناسه یکتا برای کار با استفاده از timestamp و عدد تصادفی."""
        return f"{int(time.time() * 1000)}_{os.urandom(4).hex()}"

    def is_completed(self):
        """بررسی می‌کند که آیا کار انجام شده است."""
        return self.status == "انجام شده"

    def is_overdue(self):
        """بررسی می‌کند که آیا کار گذشته از موعد است."""
        if not self.due_date or self.is_completed():
            return False
        try:
            due = datetime.fromisoformat(self.due_date).date()
            today = datetime.now().date()
            return due < today
        except (ValueError, TypeError):
            return False

    def is_due_today(self):
        """بررسی می‌کند که آیا کار امروز سررسید دارد."""
        if not self.due_date or self.is_completed():
            return False
        try:
            due = datetime.fromisoformat(self.due_date).date()
            today = datetime.now().date()
            return due == today
        except (ValueError, TypeError):
            return False

    def get_due_status(self):
        """وضعیت سررسید کار را برمی‌گرداند."""
        if not self.due_date or self.is_completed():
            return "-"
        if self.is_overdue():
            return "دیرکرد"
        if self.is_due_today():
            return "امروز"
        return ""

    def get_formatted_due_date(self):
        """تاریخ سررسید را به صورت فرمت شده برمی‌گرداند."""
        if not self.due_date:
            return ""
        try:
            due = datetime.fromisoformat(self.due_date).date()
            today = datetime.now().date()
            delta = (due - today).days

            if delta == 0:
                return "امروز"
            elif delta == 1:
                return "فردا"
            elif delta == -1:
                return "دیروز"
            elif delta > 0 and delta <= 7:
                return f"{delta} روز دیگر"
            elif delta < 0 and delta >= -7:
                return f"{abs(delta)} روز پیش"
            else:
                return self.due_date
        except (ValueError, TypeError):
            return self.due_date or ""

    def has_subtasks(self):
        """بررسی می‌کند که آیا کار دارای زیرکار است."""
        return len(self.subtasks) > 0

    def get_subtask_progress(self):
        """پیشرفت زیرکارها را برمی‌گرداند (تعداد انجام شده / کل)."""
        if not self.has_subtasks():
            return None
        completed = sum(1 for st in self.subtasks if st.is_completed())
        total = len(self.subtasks)
        return (completed, total)

    def to_list(self):
        """یک کار را برای نوشتن در فایل CSV به لیست تبدیل می‌کند."""
        # رمزگذاری notes به base64
        notes_encoded = ""
        if self.notes:
            notes_encoded = base64.b64encode(self.notes.encode('utf-8')).decode('utf-8')

        # تبدیل recurrence_pattern به JSON
        recurrence_json = ""
        recurrence_type = ""
        recurrence_interval = ""
        recurrence_weekdays = ""
        recurrence_end_date = ""

        if self.is_recurring and self.recurrence_pattern:
            recurrence_type = self.recurrence_pattern.get("type", "")
            recurrence_interval = str(self.recurrence_pattern.get("interval", ""))
            weekdays = self.recurrence_pattern.get("weekdays", [])
            recurrence_weekdays = ",".join(map(str, weekdays)) if weekdays else ""
            recurrence_end_date = self.recurrence_pattern.get("end_date", "") or ""

        return [
            self.task_id,
            self.name,
            self.description,
            self.priority,
            self.status,
            self.completion_date or "",
            self.due_date or "",
            self.category or "بدون دسته",
            self.parent_id or "",
            str(self.subtask_order) if self.subtask_order is not None else "",
            "true" if self.is_recurring else "false",
            recurrence_type,
            recurrence_interval,
            recurrence_weekdays,
            recurrence_end_date,
            notes_encoded
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
