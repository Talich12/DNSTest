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
        TRUNCATE TABLE stores;
        
        INSERT INTO stores ("Branch_ID", "Priority")
        SELECT DISTINCT ON ("Фирма")
			"Фирма" AS "Branch_ID",
            FLOOR(RANDOM() * 11)::integer AS "Priority"
        FROM 
            branch_product;
    """)
    
    # Подтверждаем изменения
    conn.commit()
    print("Таблица stores успешно заполнена случайными приоритетами (0-10)")
    
except Exception as e:
    print(f"Ошибка: {e}")
    conn.rollback()
    
finally:
    cursor.close()
    conn.close()