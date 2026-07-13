from typing import Dict
from modelos.candidato import Candidato
from servicios.autenticacion import ServicioAutenticacion
from servicios.gestor_archivos import GestorArchivos

class SistemaElectoral:
    """Controlador que gestiona el proceso de votación con persistencia de datos."""
    
    ARCHIVO_DATOS = "datos/resultados.json"

    def __init__(self):
        self.candidatos: Dict[int, Candidato] = {}
        self.auth_service = ServicioAutenticacion()
        self._cargar_o_inicializar_candidatos()

    def _cargar_o_inicializar_candidatos(self) -> None:
        """Intenta cargar de JSON; si no existe, crea los valores por defecto."""
        datos_guardados = GestorArchivos.cargar_datos(self.ARCHIVO_DATOS)
        
        if datos_guardados:
            for id_str, datos in datos_guardados.items():
                cand = Candidato(int(id_str), datos["nombre"], datos["partido"])
                cand.votos = datos["votos"]
                self.candidatos[cand.id] = cand
        else:
            lista_inicial = [
                Candidato(1, "Ana Martínez", "Partido Tecnológico"),
                Candidato(2, "Carlos Mendoza", "Unión Digital"),
                Candidato(3, "Voto en Blanco", "N/A")
            ]
            for c in lista_inicial:
                self.candidatos[c.id] = c
            self._guardar_estado()

    def _guardar_estado(self) -> None:
        """Convierte los objetos a diccionario y los guarda en JSON."""
        datos_exportar = {}
        for cand in self.candidatos.values():
            datos_exportar[cand.id] = {
                "nombre": cand.nombre,
                "partido": cand.partido,
                "votos": cand.votos
            }
        GestorArchivos.guardar_datos(self.ARCHIVO_DATOS, datos_exportar)

    def registrar_voto(self, dni: str, id_candidato: int) -> bool:
        """Valida, inserta el voto y guarda físicamente el cambio."""
        if id_candidato not in self.candidatos:
            raise KeyError("La opción de voto seleccionada no es válida.")

        # Lógica transaccional
        self.auth_service.marcar_como_votado(dni)
        self.candidatos[id_candidato].incrementar_voto()
        
        # PERSISTENCIA: Se guarda inmediatamente en el disco
        self._guardar_estado()
        return True