# Quick Installation Guide

## 🚀 Fast Setup (5 Minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Run Server
```bash
python manage.py runserver
```

### Step 4: Open Browser
Navigate to: **http://127.0.0.1:8000/**

---

## 📋 Detailed Instructions

For complete setup instructions, see **[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)**

---

## ⚡ Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py makemigrations
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## 🔧 Requirements

- Python 3.8+
- pip (comes with Python)
- SQLite (included with Python) OR MySQL (optional)

---

## ✅ That's It!

The application uses SQLite by default, so no database setup is required. Just install dependencies and run!

