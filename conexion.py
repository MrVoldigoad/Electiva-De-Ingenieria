import psycopg2
from psycopg2 import pool
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔥 CREAR POOL DE CONEXIONES PARA MEJOR RENDIMIENTO
connection_pool = None

def inicializar_pool():
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,
            host="localhost",
            database="bebidas_pacifico",
            user="postgres",
            password="1109920832",
            port="5432",
            connect_timeout=5
        )
        logger.info("✅ Pool de conexiones inicializado correctamente")
    except Exception as e:
        logger.error(f"❌ Error al inicializar pool: {e}")
        connection_pool = None

def conectar():
    """Obtiene conexión del pool o crea una nueva"""
    global connection_pool
    
    try:
        if connection_pool is None:
            inicializar_pool()
        
        if connection_pool:
            return connection_pool.getconn()
        else:
            # Fallback: conexión directa
            return psycopg2.connect(
                host="localhost",
                database="bebidas_pacifico",
                user="postgres",
                password="1109920832",
                port="5432",
                connect_timeout=5
            )
    except psycopg2.OperationalError as e:
        logger.error(f"❌ Error de conexión a BD: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Error desconocido: {e}")
        raise

def devolver_conexion(conn):
    """Devuelve la conexión al pool"""
    global connection_pool
    if connection_pool:
        connection_pool.putconn(conn)
    else:
        conn.close()

def cerrar_pool():
    """Cierra el pool de conexiones"""
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        logger.info("✅ Pool de conexiones cerrado")