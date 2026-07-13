import json
import logging
import os
from typing import Dict, Any

# Configuración del log para auditoría (esencial en elecciones)
logging.basicConfig(
    filename='auditoria_electoral.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GestorArchivos:
    """Maneja la persistencia de datos combinando escritura atómica y auditoría."""
    
    @staticmethod
    def guardar_datos(ruta_archivo: str, datos: Dict[str, Any]) -> None:
        """Guarda datos de forma atómica para evitar corrupción en caso de corte eléctrico."""
        directorio = os.path.dirname(ruta_archivo)
        if directorio:
            os.makedirs(directorio, exist_ok=True)
            
        ruta_temporal = f"{ruta_archivo}.tmp"
        
        try:
            # 1. Se guarda primero en un archivo temporal
            with open(ruta_temporal, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            
            # 2. Reemplazo atómico (Operación a nivel del Sistema Operativo)
            os.replace(ruta_temporal, ruta_archivo) 
            logging.info(f"Datos guardados de forma segura en {ruta_archivo}")
            
        except (IOError, PermissionError) as e:
            logging.error(f"Error crítico de E/S al guardar en {ruta_archivo}: {e}")
            raise RuntimeError(f"Fallo crítico del sistema al guardar datos: {e}")

    @staticmethod
    def cargar_datos(ruta_archivo: str) -> dict:
        """Carga datos con recuperación automática si el archivo está corrupto."""
        if not os.path.exists(ruta_archivo):
            logging.warning(f"Archivo {ruta_archivo} no encontrado. Se iniciará el sistema en cero.")
            return {}
            
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
                
        except json.JSONDecodeError as e:
            # Aislamiento del archivo dañado para no perder evidencia
            ruta_corrupta = f"{ruta_archivo}.corrupto"
            os.rename(ruta_archivo, ruta_corrupta)
            logging.critical(f"Archivo JSON corrupto. Se aisló como {ruta_corrupta}. Error: {e}")
            raise ValueError(f"El archivo base estaba corrupto y fue aislado. El sistema debe reiniciarse.")