import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="test",
    user="postgres",
    password="admin",
    host="localhost"
)
cursor = conn.cursor()

try:
    # Выполняем SQL-запрос
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
    
    # Подтверждаем изменения
    conn.commit()
    print("Таблица needs успешно заполнена")
    
except Exception as e:
    print(f"Ошибка: {e}")
    conn.rollback()
    
finally:
    cursor.close()
    conn.close()