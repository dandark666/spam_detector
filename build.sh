#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install system dependencies
apt-get update
apt-get install -y build-essential

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('stopwords')"

# Collect static files
python manage.py collectstatic --noinput

# Make build.sh executable
chmod +x build.sh
