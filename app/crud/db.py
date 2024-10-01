from psycopg2 import pool
from core.config import settings

# Configura el pool de conexiones
connection_pool = pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=20,  # Ajusta según tus necesidades
    database=settings.POSTGRES_DB,
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_SERVER,
    port=settings.POSTGRES_PORT
)


def get_connection():
    try:
        return connection_pool.getconn()
    except Exception as e:
        print(f"Error obteniendo conexión del pool: {e}")
        raise


def release_connection(conn):
    try:
        connection_pool.putconn(conn)
    except Exception as e:
        print(f"Error liberando conexión al pool: {e}")
        raise
