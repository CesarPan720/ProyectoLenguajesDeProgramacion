import re
from servicios.gestor_base_datos import GestorBaseDatos

class ServicioAutenticacion:
    """Gestión robusta de identidad validada directamente contra MySQL."""
    
    def __init__(self):
        self.db = GestorBaseDatos()

    def _validar_formato_dni(self, dni: str) -> bool:
        patron = r"^\d{8}$"
        return bool(re.match(patron, dni))

    def verificar_identidad(self, dni: str, fecha_nacimiento: str) -> bool:
        if not self._validar_formato_dni(dni):
            raise ValueError("El DNI debe tener estrictamente 8 dígitos numéricos.")

        if not fecha_nacimiento:
            raise ValueError("Debe ingresar su fecha de nacimiento.")

        query = "SELECT * FROM padron_electoral WHERE dni = %s"
        resultados = self.db.ejecutar_consulta(query, (dni,))

        if not resultados:
            raise PermissionError("El ciudadano no figura en el padrón electoral.")

        ciudadano = resultados[0]

        if ciudadano['votado']:
            raise PermissionError("ALERTA: Este DNI ya registra un voto emitido.")

        # MySQL devuelve un date; se compara en formato ISO (AAAA-MM-DD) contra lo ingresado.
        fecha_registrada = ciudadano['fecha_nacimiento']
        fecha_registrada_str = fecha_registrada.isoformat() if hasattr(fecha_registrada, 'isoformat') else str(fecha_registrada)
        if fecha_registrada_str != fecha_nacimiento:
            raise PermissionError("La fecha de nacimiento no coincide con el registro electoral.")

        return True

    def marcar_como_votado(self, dni: str) -> None:
        """Actualiza el estado en MySQL de forma transaccional."""
        query = "UPDATE padron_electoral SET votado = TRUE WHERE dni = %s"
        self.db.ejecutar_transaccion(query, (dni,))