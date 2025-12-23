# Task Management System - Complete Setup Instructions

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Database Setup](#database-setup)
4. [Running the Application](#running-the-application)
5. [Accessing the Application](#accessing-the-application)
6. [Troubleshooting](#troubleshooting)
7. [Project Structure](#project-structure)

---

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

### Required:
- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** (Python package manager) - Usually comes with Python
- **Git** (optional) - For version control

### Optional (for MySQL):
- **MySQL Server** - [Download MySQL](https://dev.mysql.com/downloads/mysql/)
- **MySQL Workbench** (optional) - For database management

### Verify Installation:
```bash
# Check Python version
python --version
# Should show Python 3.8 or higher

# Check pip version
pip --version
```

---

## 📦 Installation Steps

### Step 1: Navigate to Project Directory

**Windows:**
```cmd
cd "C:\Users\dell\Downloads\web app"
```

**Linux/Mac:**
```bash
cd /path/to/web\ app
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Note:** Your prompt should show `(venv)` when activated.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Collecting Django>=4.2.7
  Downloading Django-4.2.7...
Installing collected packages: Django, ...
Successfully installed Django-4.2.7 ...
```

### Step 4: Verify Installation

```bash
python manage.py --version
# Should show Django version
```

---

## 💾 Database Setup

### Option A: Using SQLite (Default - Easiest)

SQLite is included with Python and requires **no additional setup**. The database file (`db.sqlite3`) will be created automatically.

**Advantages:**
- No installation required
- Works immediately
- Perfect for development

**No configuration needed!** Skip to [Running Migrations](#running-migrations).

### Option B: Using MySQL (Optional)

#### 1. Install MySQL Server
- Download and install MySQL from [mysql.com](https://dev.mysql.com/downloads/mysql/)
- Remember your MySQL root password

#### 2. Create Database

Open MySQL Command Line or MySQL Workbench and run:

```sql
CREATE DATABASE taskmanager_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 3. Install MySQL Python Packages

```bash
pip install PyMySQL
# OR
pip install mysql-connector-python
```

#### 4. Configure Database Settings

Edit `taskmanager/settings.py`:

**For PyMySQL:**
```python
# Add at the top of taskmanager/__init__.py:
import pymysql
pymysql.install_as_MySQLdb()

# In taskmanager/settings.py, update DATABASES:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'taskmanager_db',
        'USER': 'root',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

**For mysql-connector-python:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'taskmanager_db',
        'USER': 'root',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## 🚀 Running the Application

### Step 1: Create Database Migrations

```bash
python manage.py makemigrations
```

**Expected Output:**
```
Migrations for 'tasks':
  tasks/migrations/0001_initial.py
    + Create model Client
    + Create model Task
```

### Step 2: Apply Migrations

```bash
python manage.py migrate
```

**Expected Output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, tasks
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying tasks.0001_initial... OK
```

### Step 3: Create Superuser (Optional - for Admin Panel)

```bash
python manage.py createsuperuser
```

**Follow the prompts:**
```
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.
```

### Step 4: Start Development Server

```bash
python manage.py runserver
```

**Expected Output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 4.2.7, using settings 'taskmanager.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**Note:** The server runs on `http://127.0.0.1:8000/` by default.

---

## 🌐 Accessing the Application

### Main Application
- **URL:** http://127.0.0.1:8000/
- **Description:** Task Management Dashboard
- **Features:**
  - View all clients
  - Create new clients
  - Manage tasks
  - Track progress with circular progress bars
  - Search clients

### Admin Panel
- **URL:** http://127.0.0.1:8000/admin/
- **Login:** Use superuser credentials created in Step 3
- **Features:**
  - Manage clients and tasks
  - View database records
  - User management

### Alternative URLs
- http://localhost:8000/
- http://0.0.0.0:8000/ (accessible from network)

---

## 🎯 Quick Start Guide

### First Time Setup (Complete Process)

```bash
# 1. Navigate to project
cd "C:\Users\dell\Downloads\web app"

# 2. Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create migrations
python manage.py makemigrations

# 5. Apply migrations
python manage.py migrate

# 6. Create superuser (optional)
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

### Daily Usage

```bash
# Activate virtual environment (if using)
venv\Scripts\activate

# Start server
python manage.py runserver

# Open browser to http://127.0.0.1:8000/
```

---

## 🛠️ Troubleshooting

### Issue 1: "No module named 'django'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue 2: "ModuleNotFoundError: No module named 'MySQLdb'"

**Solution:**
```bash
pip install PyMySQL
```

Then add to `taskmanager/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Issue 3: "Port 8000 is already in use"

**Solution:**
```bash
# Use a different port
python manage.py runserver 8001
```

### Issue 4: "Database is locked" (SQLite)

**Solution:**
- Close all database connections
- Restart the server
- If persistent, delete `db.sqlite3` and run migrations again

### Issue 5: "Migration conflicts"

**Solution:**
```bash
# Delete migration files (except __init__.py)
# Then recreate:
python manage.py makemigrations
python manage.py migrate
```

### Issue 6: Static files not loading

**Solution:**
```bash
# For development, ensure DEBUG = True in settings.py
# For production:
python manage.py collectstatic
```

### Issue 7: MySQL Connection Error

**Solutions:**
1. Verify MySQL server is running
2. Check database credentials in `settings.py`
3. Ensure database exists:
   ```sql
   CREATE DATABASE taskmanager_db;
   ```
4. Test connection:
   ```bash
   python manage.py dbshell
   ```

---

## 📁 Project Structure

```
web app/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── SETUP_INSTRUCTIONS.md     # This file
├── README.md                 # Project overview
├── setup.bat                 # Windows setup script
├── .gitignore               # Git ignore rules
│
├── taskmanager/              # Main project directory
│   ├── __init__.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
│
├── tasks/                    # Tasks application
│   ├── __init__.py
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Database models (Client, Task)
│   ├── views.py             # View functions
│   ├── urls.py              # App URL patterns
│   ├── migrations/          # Database migrations
│   └── templates/           # HTML templates
│       └── tasks/
│           ├── base.html
│           └── dashboard.html
│
├── static/                   # Static files (CSS, JS)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
└── db.sqlite3               # SQLite database (created after migrate)
```

---

## 🔐 Security Notes

### Development Mode (Current)
- `DEBUG = True` - Shows detailed error pages
- `SECRET_KEY` - Should be changed in production
- No authentication required for main app

### Production Deployment
Before deploying to production:

1. **Change SECRET_KEY:**
   ```python
   # Generate new key:
   python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **Set DEBUG = False:**
   ```python
   DEBUG = False
   ```

3. **Update ALLOWED_HOSTS:**
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

4. **Use environment variables:**
   ```python
   import os
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

---

## 📝 Common Commands Reference

```bash
# Start development server
python manage.py runserver

# Start on specific port
python manage.py runserver 8001

# Start on all interfaces (accessible from network)
python manage.py runserver 0.0.0.0:8000

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Access database shell (SQLite)
python manage.py dbshell

# Check for issues
python manage.py check

# Collect static files (production)
python manage.py collectstatic

# Show all migrations
python manage.py showmigrations
```

---

## 🎓 Additional Resources

- **Django Documentation:** https://docs.djangoproject.com/
- **Django Tutorial:** https://docs.djangoproject.com/en/stable/intro/tutorial01/
- **Python Virtual Environments:** https://docs.python.org/3/tutorial/venv.html

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Migrations created (`python manage.py makemigrations`)
- [ ] Migrations applied (`python manage.py migrate`)
- [ ] Server starts without errors (`python manage.py runserver`)
- [ ] Can access http://127.0.0.1:8000/
- [ ] Can create a client
- [ ] Can add tasks
- [ ] Progress bars display correctly
- [ ] Search functionality works

---

## 🆘 Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review Django error messages in the terminal
3. Check browser console for JavaScript errors
4. Verify all prerequisites are installed
5. Ensure database is properly configured

---

## 📄 License

This project is open source and available for personal and commercial use.

---

**Last Updated:** 2024
**Django Version:** 4.2.7+
**Python Version:** 3.8+

