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
        TRUNCATE TABLE logdays;
        
        INSERT INTO logdays ("Branch_ID", "Category_ID", "Logdays")
        SELECT 
            bp."Фирма" AS "Branch_ID",
            p."Category_ID",
            7 AS "Logdays"
        FROM 
            branch_product bp
        JOIN 
            products p ON bp."Товар" = p."Product_ID"
        GROUP BY 
            bp."Фирма", p."Category_ID";
    """)

    conn.commit()
    print("Таблица logdays успешно заполнена")
    
except Exception as e:
    print(f"Ошибка: {e}")
    conn.rollback()
    
finally:
    cursor.close()
    conn.close()