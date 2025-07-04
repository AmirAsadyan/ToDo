# app.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font

# ایمپورت به صورت نسبی اصلاح شد
from .logic import Task, ToDoList


class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("مدیریت لیست کارها")
        self.geometry("850x550")

        self.todo_list = ToDoList()

        # یک متغیر برای نگهداری مقدار انتخاب شده در دکمه‌های رادیویی
        self.priority_var = tk.StringVar(value="متوسط")

        self.delete_mode = False
        self.strikethrough_font = font.Font(family="Tahoma", size=10, overstrike=True)

        # --- تغییر جدید: اتصال کلید Enter به تابع add_task ---
        self.bind("<Return>", self.add_task)

        style = ttk.Style(self)
        style.configure("Treeview.Heading", font=("Tahoma", 10, "bold"))
        style.configure("TButton", font=("Tahoma", 10))
        style.configure("TLabel", font=("Tahoma", 10))
        style.configure("TEntry", font=("Tahoma", 10))
        style.configure(
            "Status.TLabel", foreground="blue", font=("Tahoma", 9, "italic")
        )
        style.configure("Congrats.TLabel", font=("Tahoma", 12))

        self._create_widgets()
        self._refresh_task_list()

    def _create_widgets(self):
        # فریم ورودی‌ها
        input_frame = ttk.Frame(self, padding="10")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(input_frame, text="نام کار:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(input_frame, text="توضیحات:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.desc_entry = ttk.Entry(input_frame, width=50)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="اولویت:").grid(
            row=0, column=2, padx=5, pady=5, sticky="w"
        )

        priority_frame = ttk.Frame(input_frame)
        priority_frame.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Radiobutton(
            priority_frame, text="پایین", variable=self.priority_var, value="پایین"
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            priority_frame, text="متوسط", variable=self.priority_var, value="متوسط"
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            priority_frame, text="بالا", variable=self.priority_var, value="بالا"
        ).pack(side=tk.LEFT, padx=5)

        add_button = ttk.Button(input_frame, text="افزودن کار", command=self.add_task)
        add_button.grid(row=1, column=3, padx=10, pady=10, sticky="e")
        input_frame.columnconfigure(1, weight=1)

        # فریم لیست کارها (جدول)
        list_frame = ttk.Frame(self, padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        columns = ("status", "name", "description", "priority")
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            height=15,
            selectmode="extended",
        )

        self.tree.heading("status", text="وضعیت")
        self.tree.heading("name", text="نام کار")
        self.tree.heading("description", text="توضیحات")
        self.tree.heading("priority", text="اولویت")
        self.tree.column("status", width=70, anchor="center")
        self.tree.column("name", width=150, anchor="w")
        self.tree.column("description", width=350, anchor="w")
        self.tree.column("priority", width=100, anchor="center")

        self.tree.tag_configure("بالا", background="#ffdddd")
        self.tree.tag_configure("متوسط", background="#ffffcc")
        self.tree.tag_configure("پایین", background="#ddffdd")
        self.tree.tag_configure("done", font=self.strikethrough_font, foreground="grey")

        self.tree.bind("<Button-1>", self.handle_tree_click)
        self.tree.bind("<Delete>", self.handle_delete_key)
        self.tree.bind("<Return>", self.confirm_deletion)

        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # فریم دکمه‌ها و پیام وضعیت
        action_frame = ttk.Frame(self, padding="10")
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        self.status_label = ttk.Label(action_frame, text="", style="Status.TLabel")
        self.status_label.pack(side=tk.TOP, fill=tk.X, pady=2)
        import_button = ttk.Button(
            action_frame,
            text="Import From CSV File",
            command=self.import_from_csv_dialog,
        )
        import_button.pack(side=tk.LEFT)
        delete_button = ttk.Button(
            action_frame,
            text=  "حذف کارهای انتخاب شده",
            command=self.delete_task_with_button,
        )
        delete_button.pack(side=tk.RIGHT)

    def _refresh_task_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, task in enumerate(self.todo_list.tasks):
            status_text = "☑" if task.status == "انجام شده" else "☐"
            tags = [task.priority]
            if task.status == "انجام شده":
                tags.append("done")
            values = (status_text, task.name, task.description, task.priority)
            self.tree.insert("", tk.END, iid=i, values=values, tags=tags)

    def show_congrats_popup(self):
        popup = tk.Toplevel(self)
        popup.title("تبریک!")
        popup.attributes("-toolwindow", True)
        message = "تبریک ! شما یک کار با اولویت بالا را انجام دادید"
        label = ttk.Label(popup, text=message, style="Congrats.TLabel")
        label.pack(padx=20, pady=20)
        popup.after(2000, popup.destroy)

    def handle_tree_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return

        column_id = self.tree.identify_column(event.x)
        if column_id == "#1":
            task_index = int(row_id)
            task = self.todo_list.tasks[task_index]
            if task.status == "انجام نشده" and task.priority == "بالا":
                self.show_congrats_popup()
            self.todo_list.toggle_task_status(task_index)
            self._refresh_task_list()
            return

        if self.delete_mode:
            if row_id in self.tree.selection():
                self.tree.selection_remove(row_id)
            else:
                self.tree.selection_add(row_id)
            return "break"

    def handle_delete_key(self, event):
        if not self.delete_mode:
            self.delete_mode = True
            self.status_label.config(
                text="حالت حذف فعال است. کارها را انتخاب و Enter را بزنید. (برای لغو Delete را دوباره بزنید)"
            )
        else:
            self.delete_mode = False
            self.status_label.config(text="")

    def confirm_deletion(self, event):
        if not self.delete_mode:
            return
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning(
                "انتخاب نشده", "لطفاً حداقل یک کار را برای حذف انتخاب کنید."
            )
            return
        indices_to_delete = [int(iid) for iid in selected_items]
        self.todo_list.delete_multiple_tasks(indices_to_delete)
        self._refresh_task_list()
        self.delete_mode = False
        self.status_label.config(text="")

    def delete_task_with_button(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning(
                "انتخاب نشده", "لطفاً حداقل یک کار را برای حذف انتخاب کنید."
            )
            return
        answer = messagebox.askyesno(
            "تایید حذف", f"آیا از حذف {len(selected_items)} کار انتخاب شده مطمئن هستید؟"
        )
        if answer:
            indices_to_delete = [int(iid) for iid in selected_items]
            self.todo_list.delete_multiple_tasks(indices_to_delete)
            self._refresh_task_list()

    # --- تغییر جدید: اضافه کردن event=None به عنوان آرگومان ---
    def add_task(self, event=None):
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        priority = self.priority_var.get()
        if not name:
            messagebox.showwarning("ورودی نامعتبر", "نام کار نمی‌تواند خالی باشد.")
            return
        new_task = Task(name, desc, priority)
        self.todo_list.add_task(new_task)
        self._refresh_task_list()
        self.name_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        # برای اینکه فوکوس روی ورودی نام کار باقی بماند
        self.name_entry.focus_set()

    def import_from_csv_dialog(self):
        filepath = filedialog.askopenfilename(
            title="یک فایل CSV را انتخاب کنید",
            # خط زیر اصلاح شد
            filetypes=(("CSV Files", "*.csv"), ("All files", "*.*")),
        )
        if not filepath:
            return
        success, message = self.todo_list.import_from_csv(filepath)
        if success:
            messagebox.showinfo("موفقیت", message)
            self._refresh_task_list()
        else:
            messagebox.showerror("خطا", message)


def main():
    """تابع اصلی برای اجرای برنامه"""
    app = TodoApp()
    app.mainloop()


if __name__ == "__main__":
    main()
