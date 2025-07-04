@echo off
echo Запуск import_logdays.py...
python import_logdays.py

echo Запуск import_needs.py...
python import_needs.py

echo Запуск import_stores.py...
python import_stores.py

exit /b 0