import psycopg2
from psycopg2.extras import execute_values
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def add_to_db(name, vector):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        execute_values(
            cursor,
            "INSERT INTO faces (name, vector) VALUES %s",
            [(name, vector)]
        )

        conn.commit()

    except Exception as e:
        print(f"Ошибка при добавлении в БД: {e}")
        if 'conn' in locals():
            conn.rollback()
        raise
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()


def get_from_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        cursor.execute("SELECT name, vector FROM faces")
        faces = cursor.fetchall()

        if not faces:
            print("Нет данных для обработки")
            return []

        return faces

    except Exception as e:
        print(f"Ошибка при получении из БД: {e}")
        if 'conn' in locals():
            conn.rollback()
        raise
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()
