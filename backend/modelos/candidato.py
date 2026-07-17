class Candidato:
    """Representa a un candidato en el proceso electoral."""
    def __init__(self, id_candidato: int, nombre: str, partido: str, simbolo: str = None, foto: str = None):
        self.id = id_candidato
        self.nombre = nombre
        self.partido = partido
        self.simbolo = simbolo
        self.foto = foto
        self.votos = 0

    def incrementar_voto(self) -> None:
        """Suma un voto al candidato encapsulando la modificación."""
        self.votos += 1