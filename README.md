# 📝 ToDo App

A modern, themeable ToDo application built with Python and Tkinter, packaged for easy installation and use.

## ✨ Features

- **Create & Manage Tasks:** Add tasks with a name, description, and priority level (low, medium, high).
- **Theming:** Switch between a sleek **dark mode** and a clean **light mode**.
- **SVG Icons:** A polished user interface with scalable SVG icons.
- **Task Prioritization:** Tasks are color-coded based on their priority.
- **Status Toggling:** Mark tasks as completed with a single click.
- **Persistent Storage:** Tasks are automatically saved to a local `tasks.csv` file.
- **CSV Import:** Easily import a list of tasks from a CSV file.
- **Auto-Cleanup:** Completed tasks older than 24 hours are automatically removed.
- **Easy Installation:** Packaged as a standard Python application, installable via `pip`.

## 📂 Project Structure

```bash
ToDo/
│
├── todo_app/
│ ├── icons/
│ │ ├── add.svg
│ │ ├── delete.svg
│ │ ├── import.svg
│ │ └── theme_icon.svg
│ │
│ ├── init.py
│ ├── app.py
│ └── logic.py
│
├── .gitignore
├── LICENSE
├── MANIFEST.in
├── README.md
├── requirements.txt
└── setup.py
```

## 🚀 Installation & Usage

### Prerequisites

- **Python 3.8+**
- `pip` and `venv` (usually included with Python)

### Setup Steps

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/AmirAsadyan/ToDo.git](https://github.com/AmirAsadyan/ToDo.git)
    cd ToDo
    ```

2.  **(Recommended)** Create and activate a virtual environment:

    ```bash
    # On Windows
    python -m venv venv
    venv\Scripts\activate

    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the application:**
    The following command reads the `setup.py` file, installs all dependencies from `requirements.txt`, and makes the app available as a command-line tool.
    ```bash
    pip install .
    ```

### Running the App

After a successful installation, you can run the application from anywhere in your terminal by simply typing:

```bash
todo
```

🗑️ Uninstalling
To completely remove the application and its command from your system, run:

```bash
pip uninstall todo_app
```

