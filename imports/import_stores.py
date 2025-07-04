import psycopg2
import json


with open('./../config.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

conn = psycopg2.connect(
    dbname=data['dbname'],
    user=data['user'],
    password=data['password'],
    host=data['host']
)
cursor = conn.cursor()

try:
    cursor.execute("""
        TRUNCATE TABLE stores;
        
        INSERT INTO stores ("Branch_ID", "Priority")
        SELECT DISTINCT ON ("Фирма")
			"Фирма" AS "Branch_ID",
            FLOOR(RANDOM() * 11)::integer AS "Priority"
        FROM 
            branch_product;
    """)

    conn.commit()
    print("Таблица stores успешно заполнена случайными приоритетами (0-10)")
    
except Exception as e:
    print(f"Ошибка: {e}")
    conn.rollback()
    
finally:
    cursor.close()
    conn.close()