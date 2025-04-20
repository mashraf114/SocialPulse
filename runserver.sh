#!/bin/bash

echo "🔍 Checking if port 8000 is in use..."

# Kill any process using port 8000
fuser -k 8000/tcp > /dev/null 2>&1

echo "✅ Port 8000 is now free."
echo "🚀 Starting Django server on http://localhost:8000 ..."
python manage.py runserver
