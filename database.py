"""
Módulo de configuración de base de datos
Proporciona la conexión segura a Oracle Database
"""

import oracledb
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Credenciales de la base de datos
ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_DSN = os.getenv("ORACLE_DSN")


def get_connection():
    """
    Establece y retorna una conexión a la base de datos Oracle.
    
    Returns:
        oracledb.Connection: Objeto de conexión a Oracle
        
    Raises:
        oracledb.DatabaseError: Si hay un error al conectar
    """
    try:
        connection = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN
        )
        return connection
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error de conexión a Oracle: {error.message}")
        raise


def test_connection() -> bool:
    """
    Prueba la conexión a la base de datos.
    
    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT SYSDATE FROM DUAL")
                result = cursor.fetchone()
                print(f"✓ Conexión exitosa a Oracle. Fecha del servidor: {result[0]}")
                return True
    except Exception as e:
        print(f"✗ Error al conectar con Oracle: {e}")
        return False


if __name__ == "__main__":
    print("Probando conexión a Oracle Database...")
    test_connection()
