@echo off
echo Запуск script1.py...
python import_logdays.py

echo Запуск script2.py...
python import_needs.py

echo Запуск script3.py...
python import_stores.py

exit /b 0