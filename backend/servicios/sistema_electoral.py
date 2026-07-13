from typing import Dict
from modelos.candidato import Candidato
from servicios.autenticacion import ServicioAutenticacion
from servicios.gestor_base_datos import GestorBaseDatos

class SistemaElectoral:
    """Controlador que gestiona el proceso de votación con persistencia en MySQL."""
    
    def __init__(self):
        self.candidatos: Dict[int, Candidato] = {}
        self.auth_service = ServicioAutenticacion()
        self.db = GestorBaseDatos()
        self.cargar_candidatos()

    def cargar_candidatos(self) -> None:
        """Carga los candidatos actuales desde MySQL a la memoria."""
        self.candidatos.clear()
        query = "SELECT * FROM candidatos"
        registros = self.db.ejecutar_consulta(query)
        
        for fila in registros:
            cand = Candidato(fila['id_candidato'], fila['nombre'], fila['partido'])
            cand.votos = fila['votos']
            self.candidatos[cand.id] = cand

    def registrar_voto(self, dni: str, id_candidato: int) -> bool:
        """Valida e inserta el voto directamente en la base de datos MySQL."""
        self.cargar_candidatos()
        
        if id_candidato not in self.candidatos:
            raise KeyError("La opción de voto seleccionada no es válida.")

        # Transacción segura en dos pasos
        self.auth_service.marcar_como_votado(dni)
        
        # Actualizamos el voto en MySQL
        query = "UPDATE candidatos SET votos = votos + 1 WHERE id_candidato = %s"
        self.db.ejecutar_transaccion(query, (id_candidato,))
        
        # Actualizamos la memoria local para el reporte inmediato
        self.candidatos[id_candidato].incrementar_voto()
        return True