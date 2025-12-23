#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Install Vercel CLI
npm install --global vercel@latest

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

# Create a superuser (optional, you'll need to handle this securely in production)
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell
