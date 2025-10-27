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
        self.categories = set()
        self._default_categories = ["بدون دسته", "کاری", "شخصی", "خانه", "خرید", "مطالعه"]
        self.categories.update(self._default_categories)
        self._load_tasks()
        # در ابتدای اجرای برنامه، کارهای قدیمی را پاک کن
        # self._cleanup_old_tasks()  # Will be replaced with configurable cleanup

    def _load_tasks(self):
        """کارها را از فایل CSV اصلی برنامه بارگذاری می‌کند."""
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader, None)

                for row in reader:
                    if not row:
                        continue

                    # پشتیبانی از فرمت جدید (16 ستون)
                    if len(row) >= 16:
                        # رمزگشایی notes از base64
                        notes = ""
                        if row[15]:
                            try:
                                notes = base64.b64decode(row[15]).decode('utf-8')
                            except Exception:
                                notes = ""

                        # ساخت recurrence_pattern از ستون‌های CSV
                        recurrence_pattern = None
                        is_recurring = row[10].lower() == "true"
                        if is_recurring and row[11]:
                            recurrence_pattern = {
                                "type": row[11],
                                "interval": int(row[12]) if row[12] else 1,
                                "weekdays": [int(d) for d in row[13].split(",")] if row[13] else [],
                                "end_date": row[14] if row[14] else None
                            }

                        task = Task(
                            task_id=row[0],
                            name=row[1],
                            description=row[2],
                            priority=row[3],
                            status=row[4],
                            completion_date=row[5] if row[5] else None,
                            due_date=row[6] if row[6] else None,
                            category=row[7] if row[7] else "بدون دسته",
                            parent_id=row[8] if row[8] else None,
                            subtask_order=int(row[9]) if row[9] else None,
                            is_recurring=is_recurring,
                            recurrence_pattern=recurrence_pattern,
                            notes=notes
                        )

                        # افزودن دسته‌بندی به لیست دسته‌بندی‌ها
                        if task.category:
                            self.categories.add(task.category)

                        self.tasks.append(task)

                    # پشتیبانی از فرمت قدیمی (5 ستون)
                    elif len(row) == 5:
                        completion_date = row[4] if row[4] else None
                        task = Task(
                            name=row[0],
                            description=row[1],
                            priority=row[2],
                            status=row[3],
                            completion_date=completion_date,
                        )
                        self.tasks.append(task)

                    # پشتیبانی از فرمت قدیمی‌تر (4 ستون)
                    elif len(row) == 4:
                        task = Task(
                            name=row[0],
                            description=row[1],
                            priority=row[2],
                            status=row[3],
                        )
                        self.tasks.append(task)

                # ساخت ساختار زیرکار بر اساس parent_id
                self._build_subtask_hierarchy()

        except Exception as e:
            print(f"خطا در بارگذاری فایل: {e}")

    def _save_tasks(self):
        """کل لیست کارها را در فایل CSV اصلی برنامه ذخیره می‌کند."""
        try:
            with open(self.filename, mode="w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                # نوشتن هدر جدید با تمام ستون‌ها
                writer.writerow([
                    "TaskID", "Name", "Description", "Priority", "Status",
                    "CompletionDate", "DueDate", "Category", "ParentID", "SubtaskOrder",
                    "IsRecurring", "RecurrenceType", "RecurrenceInterval",
                    "RecurrenceWeekdays", "RecurrenceEndDate", "Notes"
                ])

                # ذخیره کارهای والد ابتدا، سپس زیرکارها
                def write_task_and_subtasks(task):
                    writer.writerow(task.to_list())
                    for subtask in task.subtasks:
                        write_task_and_subtasks(subtask)

                # نوشتن فقط کارهای ریشه (بدون parent)
                for task in self.tasks:
                    if not task.parent_id:
                        write_task_and_subtasks(task)

        except Exception as e:
            print(f"خطا در ذخیره فایل: {e}")

    def _build_subtask_hierarchy(self):
        """ساختار زیرکارها را بر اساس parent_id می‌سازد."""
        # ایجاد دیکشنری برای دسترسی سریع به کارها بر اساس task_id
        task_dict = {task.task_id: task for task in self.tasks}

        # پیدا کردن زیرکارها و افزودن به والدشان
        for task in self.tasks:
            if task.parent_id and task.parent_id in task_dict:
                parent = task_dict[task.parent_id]
                parent.subtasks.append(task)

        # مرتب‌سازی زیرکارها بر اساس subtask_order
        for task in self.tasks:
            if task.subtasks:
                task.subtasks.sort(key=lambda st: st.subtask_order if st.subtask_order is not None else 0)

    def get_all_categories(self):
        """لیست مرتب شده از تمام دسته‌بندی‌ها را برمی‌گرداند."""
        return sorted(list(self.categories))

    def add_category(self, category_name):
        """یک دسته‌بندی جدید اضافه می‌کند."""
        if category_name and category_name.strip():
            self.categories.add(category_name.strip())

    def update_task(self, index, updated_task):
        """یک کار را به‌روز می‌کند."""
        if 0 <= index < len(self.tasks):
            # حفظ task_id اصلی
            original_task_id = self.tasks[index].task_id
            updated_task.task_id = original_task_id

            # جایگزینی کار
            self.tasks[index] = updated_task

            # افزودن دسته‌بندی جدید اگر وجود ندارد
            if updated_task.category:
                self.add_category(updated_task.category)

            self._save_tasks()
            return True
        return False

    def _cleanup_old_tasks(self, config=None):
        """کارهای قدیمی را بر اساس تنظیمات پاکسازی حذف می‌کند."""
        if config is None:
            # استفاده از تنظیمات پیش‌فرض (رفتار قدیمی)
            config = {
                "enabled": True,
                "days_old": 1,
                "status_filter": "completed",
                "priority_filter": [],
                "exclude_categories": []
            }

        if not config.get("enabled", False):
            return []

        now = datetime.now()
        days_old = config.get("days_old", 1)
        status_filter = config.get("status_filter", "completed")
        priority_filter = config.get("priority_filter", [])
        exclude_cats = config.get("exclude_categories", [])
        cutoff_date = now - timedelta(days=days_old)

        tasks_to_keep = []
        tasks_cleaned = []

        for task in self.tasks:
            should_cleanup = False

            # بررسی دسته‌بندی استثنا شده
            if task.category in exclude_cats:
                tasks_to_keep.append(task)
                continue

            # بررسی فیلتر وضعیت
            if status_filter == "completed" and task.status != "انجام شده":
                tasks_to_keep.append(task)
                continue
            if status_filter == "incomplete" and task.status == "انجام شده":
                tasks_to_keep.append(task)
                continue

            # بررسی فیلتر اولویت
            if priority_filter and task.priority not in priority_filter:
                tasks_to_keep.append(task)
                continue

            # بررسی سن کار
            if status_filter == "completed" and task.completion_date:
                try:
                    completion_time = datetime.fromisoformat(task.completion_date)
                    if completion_time < cutoff_date:
                        should_cleanup = True
                except (ValueError, TypeError):
                    pass

            if should_cleanup:
                tasks_cleaned.append(task)
            else:
                tasks_to_keep.append(task)

        # به‌روزرسانی لیست کارها
        if tasks_cleaned:
            self.tasks = tasks_to_keep
            self._save_tasks()

        return tasks_cleaned

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
