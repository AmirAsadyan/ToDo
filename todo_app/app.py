# app.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
import os
import tksvg

from .logic import Task, ToDoList


# ------------------ مدیریت آیکون ------------------
class IconManager:
    """کلاسی برای مدیریت و بارگذاری آیکون‌ها."""

    def __init__(self, icons_path):
        self.icons_path = icons_path
        self.icons = {}

    def get_icon(self, name, scale=1.0):
        if name in self.icons:
            return self.icons[name]

        filepath = os.path.join(self.icons_path, name)
        try:
            icon_image = tksvg.SvgImage(file=filepath, scaletowidth=int(20 * scale))
            self.icons[name] = icon_image
            return icon_image
        except Exception as e:
            print(f"خطا در بارگذاری آیکون '{filepath}': {e}")
            return None


# ------------------ مدیریت تم ------------------
class ThemeManager:
    """کلاسی برای مدیریت تم‌های روشن و تاریک."""

    def __init__(self, app):
        self.app = app
        self.style = app.style
        self.light_theme = {
            "bg": "#f0f0f0",
            "fg": "#000000",
            "entry_bg": "#ffffff",
            "tree_bg": "#ffffff",
            "tree_fg": "#000000",
            "tree_heading_bg": "#dddddd",
            "high_priority_bg": "#ffdddd",
            "medium_priority_bg": "#ffffcc",
            "low_priority_bg": "#ddffdd",
            "done_fg": "grey",
            "button_bg": "#e1e1e1",
        }
        self.dark_theme = {
            "bg": "#2b2b2b",
            "fg": "#ffffff",
            "entry_bg": "#3c3f41",
            "tree_bg": "#3c3f41",
            "tree_fg": "#ffffff",
            "tree_heading_bg": "#444444",
            "high_priority_bg": "#8b0000",
            "medium_priority_bg": "#6b6b00",
            "low_priority_bg": "#006400",
            "done_fg": "#a9a9a9",
            "button_bg": "#555555",
        }

    def apply_theme(self):
        theme = (
            self.light_theme if self.app.current_theme == "light" else self.dark_theme
        )
        self.app.config(bg=theme["bg"])
        self.style.theme_use("clam")
        self.style.configure(
            ".", background=theme["bg"], foreground=theme["fg"], font=("Tahoma", 10)
        )
        self.style.configure("TFrame", background=theme["bg"])
        self.style.configure("TLabel", background=theme["bg"], foreground=theme["fg"])
        self.style.configure(
            "TRadiobutton", background=theme["bg"], foreground=theme["fg"]
        )
        self.style.configure(
            "TButton",
            background=theme["button_bg"],
            foreground=theme["fg"],
            font=("Tahoma", 10),
        )
        self.style.map("TButton", background=[("active", theme["entry_bg"])])
        self.style.configure(
            "TEntry",
            fieldbackground=theme["entry_bg"],
            foreground=theme["fg"],
            insertcolor=theme["fg"],
        )
        self.style.configure(
            "Treeview",
            background=theme["tree_bg"],
            foreground=theme["tree_fg"],
            fieldbackground=theme["tree_bg"],
            rowheight=25,
        )
        self.style.configure(
            "Treeview.Heading",
            font=("Tahoma", 10, "bold"),
            background=theme["tree_heading_bg"],
            foreground=theme["fg"],
        )
        self.app.task_list_frame.tree.tag_configure(
            "بالا", background=theme["high_priority_bg"], foreground=theme["fg"]
        )
        self.app.task_list_frame.tree.tag_configure(
            "متوسط", background=theme["medium_priority_bg"], foreground=theme["fg"]
        )
        self.app.task_list_frame.tree.tag_configure(
            "پایین", background=theme["low_priority_bg"], foreground=theme["fg"]
        )
        self.app.task_list_frame.tree.tag_configure("done", foreground=theme["done_fg"])


# ------------------ فریم ورودی‌ها (آپدیت شده) ------------------
class InputFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding="10")
        self.controller = controller

        # ردیف اول: نام و اولویت
        ttk.Label(self, text="نام کار:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.name_entry = ttk.Entry(self, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="اولویت:").grid(
            row=0, column=2, padx=5, pady=5, sticky="w"
        )
        priority_frame = ttk.Frame(self)
        priority_frame.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(
            priority_frame,
            text="پایین",
            variable=controller.priority_var,
            value="پایین",
        ).pack(side=tk.LEFT)
        ttk.Radiobutton(
            priority_frame,
            text="متوسط",
            variable=controller.priority_var,
            value="متوسط",
        ).pack(side=tk.LEFT)
        ttk.Radiobutton(
            priority_frame, text="بالا", variable=controller.priority_var, value="بالا"
        ).pack(side=tk.LEFT)

        # ردیف دوم: توضیحات
        ttk.Label(self, text="توضیحات:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.desc_entry = ttk.Entry(self, width=50)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # ردیف سوم: تاریخ سررسید و دسته‌بندی
        ttk.Label(self, text="تاریخ سررسید (YYYY-MM-DD):").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        self.due_date_entry = ttk.Entry(self, width=20)
        self.due_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.due_date_entry.insert(0, "")

        ttk.Label(self, text="دسته‌بندی:").grid(
            row=2, column=2, padx=5, pady=5, sticky="w"
        )
        self.category_combo = ttk.Combobox(self, width=18, state="normal")
        self.category_combo.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        self.update_categories()

        # دکمه افزودن
        add_icon = self.controller.icon_manager.get_icon("Add.svg")
        add_button = ttk.Button(
            self,
            text=" افزودن",
            image=add_icon,
            compound="left",
            command=self.controller.add_task,
        )
        if not add_icon:
            add_button.config(text="افزودن کار")
        add_button.grid(row=3, column=3, padx=10, pady=10, sticky="e")

        self.columnconfigure(1, weight=1)

    def update_categories(self):
        """به‌روزرسانی لیست دسته‌بندی‌ها."""
        categories = self.controller.todo_list.get_all_categories()
        self.category_combo['values'] = categories
        if categories and "بدون دسته" in categories:
            self.category_combo.set("بدون دسته")
        elif categories:
            self.category_combo.set(categories[0])
        else:
            self.category_combo.set("بدون دسته")

    def clear_inputs(self):
        """پاک کردن تمام فیلدهای ورودی."""
        self.name_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.category_combo.set("بدون دسته")


# ------------------ فریم لیست کارها ------------------
class TaskListFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding="10")
        self.controller = controller

        # ستون‌های جدید: status, name, description, priority, category, due_date, due_status
        columns = ("status", "name", "description", "priority", "category", "due_date", "due_status")
        self.tree = ttk.Treeview(
            self, columns=columns, show="headings", height=15, selectmode="extended"
        )
        self.tree.heading("status", text="وضعیت")
        self.tree.column("status", width=60, anchor="center")
        self.tree.heading("name", text="نام کار")
        self.tree.column("name", width=150, anchor="w")
        self.tree.heading("description", text="توضیحات")
        self.tree.column("description", width=250, anchor="w")
        self.tree.heading("priority", text="اولویت")
        self.tree.column("priority", width=80, anchor="center")
        self.tree.heading("category", text="دسته‌بندی")
        self.tree.column("category", width=100, anchor="center")
        self.tree.heading("due_date", text="سررسید")
        self.tree.column("due_date", width=120, anchor="center")
        self.tree.heading("due_status", text="وضعیت سررسید")
        self.tree.column("due_status", width=100, anchor="center")

        self.tree.bind("<Button-1>", self.controller.handle_tree_click)
        self.tree.bind("<Delete>", self.controller.handle_delete_key)
        self.tree.bind("<Return>", self.controller.confirm_deletion)

        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh(self, tasks):
        """لیست کارها را بازخوانی می‌کند."""
        self.tree.delete(*self.tree.get_children())

        # پیکربندی تگ‌های رنگی برای وضعیت سررسید
        self.tree.tag_configure("overdue", background="#ffcccc")
        self.tree.tag_configure("due_today", background="#fff9cc")

        for i, task in enumerate(tasks):
            # نمایش وضعیت با آیکون تیک
            status_text = "☑" if task.is_completed() else "☐"

            # آیکون تکرارشونده
            name_display = task.name
            if task.is_recurring:
                name_display = f"🔁 {task.name}"

            # نمایش پیشرفت زیرکارها
            description_display = task.description
            if task.has_subtasks():
                progress = task.get_subtask_progress()
                if progress:
                    completed, total = progress
                    description_display = f"{task.description} ({completed}/{total} انجام شده)"

            # دسته‌بندی
            category_display = task.category if task.category else "بدون دسته"

            # تاریخ سررسید با فرمت نسبی
            due_date_display = task.get_formatted_due_date()

            # وضعیت سررسید
            due_status_display = task.get_due_status()

            # تعیین تگ‌ها برای رنگ‌آمیزی
            tags = [task.priority]
            if task.is_completed():
                tags.append("done")
            if task.is_overdue():
                tags.append("overdue")
            elif task.is_due_today():
                tags.append("due_today")

            self.tree.insert(
                "",
                tk.END,
                iid=i,
                values=(
                    status_text,
                    name_display,
                    description_display,
                    task.priority,
                    category_display,
                    due_date_display,
                    due_status_display
                ),
                tags=tags,
            )


# ------------------ فریم دکمه‌های عملیاتی (آپدیت شده) ------------------
class ActionFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding="10")
        self.controller = controller

        self.status_label = ttk.Label(self, text="")
        self.status_label.pack(side=tk.TOP, fill=tk.X, pady=2)

        theme_icon = self.controller.icon_manager.get_icon("Dark_Mode.svg")
        theme_button = ttk.Button(
            self,
            text=" تغییر تم",
            image=theme_icon,
            compound="left",
            command=self.controller.toggle_theme,
        )
        if not theme_icon:
            theme_button.config(text="تغییر تم 🌓")
        theme_button.pack(side=tk.LEFT, padx=(0, 5))

        import_icon = self.controller.icon_manager.get_icon("Import.svg")
        import_button = ttk.Button(
            self,
            text=" Import",
            image=import_icon,
            compound="left",
            command=self.controller.import_from_csv_dialog,
        )
        if not import_icon:
            import_button.config(text="Import")
        import_button.pack(side=tk.LEFT, padx=5)

        delete_icon = self.controller.icon_manager.get_icon("Delete.svg")
        delete_button = ttk.Button(
            self,
            text=" حذف",
            image=delete_icon,
            compound="left",
            command=self.controller.delete_task_with_button,
        )
        if not delete_icon:
            delete_button.config(text="حذف")
        delete_button.pack(side=tk.RIGHT, padx=5)


# ------------------ کلاس اصلی برنامه ------------------
class TodoApp(tk.Tk):
    def __init__(self, icons_path):
        super().__init__()
        self.title("مدیریت لیست کارها")

        self.todo_list = ToDoList()
        self.icon_manager = IconManager(icons_path)
        self.style = ttk.Style(self)
        self.theme_manager = ThemeManager(self)

        self.current_theme = "light"
        self.priority_var = tk.StringVar(value="متوسط")
        self.delete_mode = False

        self.bind("<Return>", lambda event: self.add_task())

        self.input_frame = InputFrame(self, self)
        self.input_frame.pack(fill=tk.X)
        self.task_list_frame = TaskListFrame(self, self)
        self.task_list_frame.pack(fill=tk.BOTH, expand=True)
        self.action_frame = ActionFrame(self, self)
        self.action_frame.pack(fill=tk.X)

        self.theme_manager.apply_theme()
        self.refresh_task_list()

        self.update_idletasks()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())

    def refresh_task_list(self):
        self.task_list_frame.refresh(self.todo_list.tasks)

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.theme_manager.apply_theme()

    def add_task(self):
        name = self.input_frame.name_entry.get()
        if not name:
            messagebox.showwarning("ورودی نامعتبر", "نام کار نمی‌تواند خالی باشد.")
            return
        self.todo_list.add_task(
            Task(name, self.input_frame.desc_entry.get(), self.priority_var.get())
        )
        self.refresh_task_list()
        self.input_frame.name_entry.delete(0, tk.END)
        self.input_frame.desc_entry.delete(0, tk.END)
        self.input_frame.name_entry.focus_set()

    def handle_tree_click(self, event):
        if self.task_list_frame.tree.identify_region(event.x, event.y) != "cell":
            return
        row_id = self.task_list_frame.tree.identify_row(event.y)
        if not row_id:
            return
        if self.task_list_frame.tree.identify_column(event.x) == "#1":
            task_index = int(row_id)
            if (
                self.todo_list.tasks[task_index].status == "انجام نشده"
                and self.todo_list.tasks[task_index].priority == "بالا"
            ):
                self.show_congrats_popup()
            self.todo_list.toggle_task_status(task_index)
            self.refresh_task_list()

    def handle_delete_key(self, event):
        self.delete_mode = not self.delete_mode
        self.action_frame.status_label.config(
            text="حالت حذف فعال است" if self.delete_mode else ""
        )

    def confirm_deletion(self, event):
        if not self.delete_mode:
            return
        selected_items = self.task_list_frame.tree.selection()
        if not selected_items:
            return
        self.delete_tasks_by_indices([int(iid) for iid in selected_items])
        self.delete_mode = False
        self.action_frame.status_label.config(text="")

    def delete_task_with_button(self):
        selected_items = self.task_list_frame.tree.selection()
        if not selected_items:
            messagebox.showwarning("انتخاب نشده", "لطفاً کاری برای حذف انتخاب کنید.")
            return
        if messagebox.askyesno(
            "تایید حذف", f"آیا از حذف {len(selected_items)} کار مطمئن هستید؟"
        ):
            self.delete_tasks_by_indices([int(iid) for iid in selected_items])

    def delete_tasks_by_indices(self, indices):
        self.todo_list.delete_multiple_tasks(indices)
        self.refresh_task_list()

    def import_from_csv_dialog(self):
        filepath = filedialog.askopenfilename(
            filetypes=(("CSV Files", "*.csv"), ("All files", "*.*"))
        )
        if not filepath:
            return
        success, message = self.todo_list.import_from_csv(filepath)
        if success:
            self.refresh_task_list()
            messagebox.showinfo("موفقیت", message)
        else:
            messagebox.showerror("خطا", message)

    def show_congrats_popup(self):
        popup = tk.Toplevel(self)
        popup.title("تبریک!")
        popup.transient(self)
        popup.grab_set()
        label = ttk.Label(
            popup,
            text="آفرین! یک کار مهم رو انجام دادی 🎉",
            font=("Tahoma", 12),
            padding=20,
        )
        label.pack()
        self.theme_manager.apply_theme()
        self.after(2000, popup.destroy)


# ------------------ تابع اصلی ------------------
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icons_path = os.path.join(script_dir, "icons")

    if not os.path.exists(icons_path):
        os.makedirs(icons_path)
        print(
            f"پوشه 'icons' در مسیر '{icons_path}' ایجاد شد. لطفاً آیکون‌ها را در آن قرار دهید."
        )

    app = TodoApp(icons_path=icons_path)
    app.mainloop()


if __name__ == "__main__":
    main()
