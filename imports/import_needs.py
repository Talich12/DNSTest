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
        TRUNCATE TABLE needs;
        
        INSERT INTO needs ("Branch_ID", "Product_ID", "Needs")
        SELECT 
			bp."Фирма" AS "Branch_ID",
			bp."Товар" AS "Product_ID",
			FLOOR(RANDOM() * (GREATEST(150, bp."Остаток") + 1)) * lg."Logdays" AS "Needs"
		FROM 
			branch_product bp
		LEFT JOIN 
			products p ON bp."Товар" = p."Product_ID"
		LEFT JOIN 
			logdays lg ON p."Category_ID" = lg."Category_ID" AND bp."Фирма" = lg."Branch_ID"

    """)

    conn.commit()
    print("Таблица needs успешно заполнена")
    
except Exception as e:
    print(f"Ошибка: {e}")
    conn.rollback()
    
finally:
    cursor.close()
    conn.close()