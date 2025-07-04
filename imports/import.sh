#!/bin/bash

echo "Запуск script1.py..."
python3 import_logdays.py

echo "Запуск script2.py..."
python3 import_needs.py

echo "Запуск script3.py..."
python3 import_stores.py

exit 0