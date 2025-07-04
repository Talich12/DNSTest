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
        WITH firms AS (
            SELECT DISTINCT "Фирма" FROM branch_product
        ),
        numbered_firms AS (
            SELECT 
                "Фирма" AS "Branch_ID",
                ROW_NUMBER() OVER (ORDER BY random()) - 1 AS "Priority"
            FROM firms
        )
        SELECT "Branch_ID", "Priority"
        FROM numbered_firms;
    """)

    conn.commit()
    print("Таблица stores успешно заполнена случайными приоритетами")
    
except Exception as e:
    print(f"Ошибка: {e}")
    conn.rollback()
    
finally:
    cursor.close()
    conn.close()