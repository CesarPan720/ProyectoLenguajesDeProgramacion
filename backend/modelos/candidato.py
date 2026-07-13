class Candidato:
    """Representa a un candidato en el proceso electoral."""
    def __init__(self, id_candidato: int, nombre: str, partido: str):
        self.id = id_candidato
        self.nombre = nombre
        self.partido = partido
        self.votos = 0

    def incrementar_voto(self) -> None:
        """Suma un voto al candidato encapsulando la modificación."""
        self.votos += 1