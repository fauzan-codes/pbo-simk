@echo off

call venv\Scripts\activate

echo Menjalankan Tailwind CSS...
start /B python manage.py tailwind start

echo Menjalankan Django Server...
python manage.py runserver
