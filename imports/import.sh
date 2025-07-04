#!/bin/bash

echo "Запуск import_logdays.py..."
python3 import_logdays.py

echo "Запуск import_needs.py..."
python3 import_needs.py

echo "Запуск import_stores.py..."
python3 import_stores.py

exit 0