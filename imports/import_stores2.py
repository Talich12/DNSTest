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
    
    # Подтверждаем изменения
    conn.commit()
    print("Таблица stores успешно заполнена случайными приоритетами")
    
except Exception as e:
    print(f"Ошибка: {e}")
    conn.rollback()
    
finally:
    cursor.close()
    conn.close()