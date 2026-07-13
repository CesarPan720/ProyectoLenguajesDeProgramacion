import re
from servicios.gestor_base_datos import GestorBaseDatos

class ServicioAutenticacion:
    """Gestión robusta de identidad validada directamente contra MySQL."""
    
    def __init__(self):
        self.db = GestorBaseDatos()

    def _validar_formato_dni(self, dni: str) -> bool:
        patron = r"^\d{8}$"
        return bool(re.match(patron, dni))

    def verificar_identidad(self, dni: str) -> bool:
        if not self._validar_formato_dni(dni):
            raise ValueError("El DNI debe tener estrictamente 8 dígitos numéricos.")

        query = "SELECT * FROM padron_electoral WHERE dni = %s"
        resultados = self.db.ejecutar_consulta(query, (dni,))

        if not resultados:
            raise PermissionError("El ciudadano no figura en el padrón electoral.")
        
        ciudadano = resultados[0]
        
        if ciudadano['votado']:
            raise PermissionError("ALERTA: Este DNI ya registra un voto emitido.")
        
        return True

    def marcar_como_votado(self, dni: str) -> None:
        """Actualiza el estado en MySQL de forma transaccional."""
        query = "UPDATE padron_electoral SET votado = TRUE WHERE dni = %s"
        self.db.ejecutar_transaccion(query, (dni,))