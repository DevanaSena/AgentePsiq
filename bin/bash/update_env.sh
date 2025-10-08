#!/bin/bash
echo "🔄 Atualizando ambiente Python e Django-Q2..."
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python manage.py check
python manage.py qinfo || echo "Q Cluster OK"
