import os
import mysql.connector
from mysql.connector import Error
import logging

logging.basicConfig(filename='auditoria_electoral.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class GestorBaseDatos:
    """Maneja las conexiones y transacciones con MySQL leyendo variables de entorno."""
    
    def __init__(self):
        # Python lee mágicamente las variables que Docker le pasa del .env
        self.host = os.getenv("DB_HOST", "mysql") 
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.database = os.getenv("DB_NAME", "elecciones_2026_peru")

    def conectar(self):
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if conexion.is_connected():
                return conexion
        except Error as e:
            logging.critical(f"Error de conexión a MySQL: {e}")
            raise RuntimeError(f"Fallo crítico: No se pudo conectar a la base de datos. {e}")

    def ejecutar_consulta(self, query: str, parametros: tuple = None) -> list:
        conexion = self.conectar()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(query, parametros or ())
            return cursor.fetchall()
        except Error as e:
            logging.error(f"Error al ejecutar consulta SELECT: {e}")
            raise
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def ejecutar_transaccion(self, query: str, parametros: tuple = None) -> None:
        conexion = self.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(query, parametros or ())
            conexion.commit()
            logging.info("Transacción exitosa completada.")
        except Error as e:
            conexion.rollback()
            logging.error(f"Error en transacción, haciendo rollback. Detalle: {e}")
            raise
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()