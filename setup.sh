#!/bin/bash

# Setup script for DocuCollab on Mac/Linux

echo "============================================="
echo "DocuCollab - Django Setup Script"
echo "============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "Step 1: Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

echo ""
echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Step 3: Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Step 4: Running database migrations..."
python manage.py migrate

echo ""
echo "Step 5: Creating admin account..."
echo "Please create a superuser account for admin access:"
python manage.py createsuperuser

echo ""
echo "============================================="
echo "Setup Complete!"
echo "============================================="
echo ""
echo "To start the development server, run:"
echo "  source venv/bin/activate (if not already active)"
echo "  python manage.py runserver"
echo ""
echo "Then open your browser to:"
echo "  http://localhost:8000"
echo ""
echo "Admin panel:"
echo "  http://localhost:8000/admin"
echo ""
