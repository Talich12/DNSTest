import psycopg2
import pandas as pd
from datetime import datetime
from uuid import UUID
import json

def distribute_products():
    with open('config.json', 'r', encoding='utf-8') as file:
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
            SELECT 
                "Товар", 
                ("Остаток" - "Резерв") AS "Используемый остаток",
                "Резерв"
            FROM rc_product
            WHERE "Остаток" > 0
        """)
        rc_products = cursor.fetchall()
        products_len = len(rc_products)
        i = 1
        for product_id, rc_quantity, reserve in rc_products:
            print(f'{i}/{products_len}')

            cursor.execute("""
                SELECT 
                    n."Branch_ID",
                    (n."Needs" - COALESCE(bp."Остаток", 0) - COALESCE(bp."Транзит", 0)) AS "Deficit",
                    s."Priority"
                FROM needs n
                LEFT JOIN branch_product bp ON n."Branch_ID" = bp."Фирма" AND n."Product_ID" = bp."Товар"
                JOIN stores s ON n."Branch_ID" = s."Branch_ID"
                WHERE n."Product_ID" = %s AND (n."Needs" - COALESCE(bp."Остаток", 0) - COALESCE(bp."Транзит", 0)) is Not null
                ORDER BY s."Priority" DESC, "Deficit" DESC
            """, (product_id,))
            
            #print(product_id, rc_quantity)
            stores_data = cursor.fetchall()
            #print(stores_data)
            if len(stores_data) > 0:
                remaining_quantity = rc_quantity

                for branch_id, deficit, priority in stores_data:
                    if remaining_quantity <= 0:
                        break
                    #print(type(branch_id))
                    quantity_to_send = min(deficit, remaining_quantity)

                    cursor.execute("""
                        UPDATE branch_product 
                        SET "Транзит" = "Транзит" + %s 
                        WHERE "Фирма" = %s AND "Товар" = %s
                    """, (quantity_to_send, branch_id, product_id))
                    
                    cursor.execute("""
                        UPDATE needs 
                        SET "Needs" = "Needs" - %s 
                        WHERE "Branch_ID" = %s AND "Product_ID" = %s
                    """, (quantity_to_send, branch_id, product_id))

                    log_distribution(cursor, product_id, branch_id, quantity_to_send)
                    remaining_quantity -= quantity_to_send
                    
                cursor.execute("""
                    UPDATE rc_product 
                    SET "Остаток" = %s
                    WHERE "Товар" = %s
                """, ((remaining_quantity + reserve), product_id))

            i+=1
  
        
        conn.commit()
        print("Распределение товаров завершено успешно.")
        
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при распределении товаров: {e}")
    finally:
        cursor.close()
        conn.close()

def log_distribution(cursor, product_id, branch_id, sended):
    cursor.execute("""
        INSERT INTO distribution_log (
            product_id, 
            branch_id, 
            sended, 
            distribution_date
        ) VALUES (%s, %s, %s, %s)
    """, (product_id, branch_id, sended, datetime.now()))


if __name__ == "__main__":
    distribute_products()