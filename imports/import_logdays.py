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
    
    # Подтверждаем изменения
    conn.commit()
    print("Таблица logdays успешно заполнена")
    
except Exception as e:
    print(f"Ошибка: {e}")
    conn.rollback()
    
finally:
    cursor.close()
    conn.close()