import re
from typing import Dict
from servicios.gestor_archivos import GestorArchivos

class ServicioAutenticacion:
    """Gestión robusta de identidad con soporte transaccional y validación RegEx."""
    
    def __init__(self):
        # Usamos directamente la ruta en la carpeta datos
        self.archivo_padron = "datos/padron.json"
        self._default_padron = {
            "70123456": {"votado": False, "biometria_registrada": True},
            "40123456": {"votado": False, "biometria_registrada": True},
            "10123456": {"votado": False, "biometria_registrada": False}
        }
        # Cargamos los datos al iniciar
        self.padron = self._cargar_o_inicializar_padron()

    def _cargar_o_inicializar_padron(self) -> Dict:
        """Carga el padrón del disco. Si no existe, crea el archivo por defecto."""
        datos = GestorArchivos.cargar_datos(self.archivo_padron)
        if not datos:
            # Si el gestor devuelve vacío, guardamos el padrón inicial
            GestorArchivos.guardar_datos(self.archivo_padron, self._default_padron)
            return self._default_padron
        return datos

    def _validar_formato_dni(self, dni: str) -> bool:
        """Validación estricta de formato usando RegEx (8 dígitos numéricos exactos)."""
        patron = r"^\d{8}$"
        return bool(re.match(patron, dni))

    def verificar_identidad(self, dni: str) -> bool:
        """
        Pase de seguridad por capas.
        AQUÍ es donde se enganchará el módulo de OpenCV/Face_Recognition:
        if self.padron[dni]['biometria_registrada']:
            self._validar_rostro_camara(dni)
        """
        if not self._validar_formato_dni(dni):
            raise ValueError("El DNI debe tener estrictamente 8 dígitos numéricos sin espacios ni letras.")

        if dni not in self.padron:
            raise PermissionError("El ciudadano no figura en el padrón electoral general.")
        
        if self.padron[dni]["votado"]:
            raise PermissionError("ALERTA DE SEGURIDAD: Este DNI ya registra un voto emitido en el sistema.")
        
        return True

    def marcar_como_votado(self, dni: str) -> None:
        """
        Guarda en disco inmediatamente que la persona ya votó.
        (Nombre ajustado para compatibilidad con SistemaElectoral)
        """
        if dni in self.padron:
            self.padron[dni]["votado"] = True
            # Llamamos al método estático de la clase GestorArchivos
            GestorArchivos.guardar_datos(self.archivo_padron, self.padron)