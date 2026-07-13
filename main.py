from servicios.sistema_electoral import SistemaElectoral
from vistas.menu_consola import ejecutar_menu_votacion

if __name__ == "__main__":
    sistema = SistemaElectoral()
    ejecutar_menu_votacion(sistema)