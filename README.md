# Task Management System

A Django web application for managing client tasks with visual circular progress indicators showing completed and remaining percentages.

## Features

- ✅ Task management in format "□ client name"
- 📊 Two circular progress bars per task:
  - Completed percentage (green)
  - Remaining percentage (orange)
- 🎨 Modern, responsive UI design
- 💾 MySQL database integration
- 🔄 Full CRUD operations (Create, Read, Update, Delete)

## Requirements

- Python 3.8+
- MySQL Server
- pip (Python package manager)

## Installation

### Quick Start (5 Minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup database
python manage.py makemigrations
python manage.py migrate

# 3. Run server
python manage.py runserver
```

**Access the application:** http://127.0.0.1:8000/

### Detailed Installation

For complete step-by-step instructions, troubleshooting, and advanced setup options, see:
- **[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** - Complete detailed guide
- **[INSTALLATION.md](INSTALLATION.md)** - Quick reference

### Key Points

- **SQLite is used by default** - No database setup required!
- **MySQL is optional** - See SETUP_INSTRUCTIONS.md for MySQL configuration
- **All dependencies** are listed in `requirements.txt`

## Usage

1. **Create a Task:**
   - Click "Add New Task" button
   - Enter client name
   - Set completed percentage using the slider
   - Click "Create Task"

2. **View Tasks:**
   - All tasks are displayed on the home page
   - Each task shows two circular progress bars:
     - Green: Completed percentage
     - Orange: Remaining percentage

3. **Update a Task:**
   - Click the edit icon on any task card
   - Modify client name or completed percentage
   - Click "Update Task"

4. **Delete a Task:**
   - Click the delete icon on any task card
   - Confirm deletion

## Project Structure

```
taskmanager/
├── manage.py
├── requirements.txt
├── taskmanager/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── tasks/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── tasks/
│           ├── base.html
│           ├── task_list.html
│           ├── task_form.html
│           └── task_confirm_delete.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Database Schema

### Task Model
- `client_name` (CharField): Name of the client
- `completed_percentage` (IntegerField): Percentage completed (0-100)
- `created_at` (DateTimeField): Task creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

## Notes

- The circular progress bars are animated using SVG and JavaScript
- The remaining percentage is automatically calculated (100 - completed_percentage)
- All tasks are displayed in reverse chronological order (newest first)

## Troubleshooting

### MySQL Connection Issues
- Ensure MySQL server is running
- Verify database credentials in `settings.py`
- Check if MySQL client libraries are installed

### Static Files Not Loading
- Run `python manage.py collectstatic` (for production)
- Ensure `STATIC_URL` and `STATICFILES_DIRS` are correctly configured

### Migration Issues
- Delete migration files and database, then recreate:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

## License

This project is open source and available for personal and commercial use.


