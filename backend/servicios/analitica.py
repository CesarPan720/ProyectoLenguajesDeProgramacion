import matplotlib.pyplot as plt
from functools import reduce
from typing import List, Dict
from modelos.candidato import Candidato

# =====================================================================
# PARADIGMA FUNCIONAL: Funciones puras, inmutabilidad y orden superior
# =====================================================================

def calcular_total_votos(candidatos: List[Candidato]) -> int:
    """Usa 'reduce' para sumar todos los votos de la lista de forma funcional."""
    if not candidatos:
        return 0
    return reduce(lambda acumulador, candidato: acumulador + candidato.votos, candidatos, 0)

def generar_reporte_porcentajes(candidatos: List[Candidato]) -> List[Dict]:
    """Usa 'map' para transformar la lista de objetos en diccionarios con porcentajes."""
    total = calcular_total_votos(candidatos)
    
    if total == 0:
        return [{"nombre": c.nombre, "votos": c.votos, "porcentaje": 0.0} for c in candidatos]

    # Función pura interna (Closure)
    def calcular_porcentaje(candidato: Candidato) -> Dict:
        porcentaje = (candidato.votos / total) * 100
        return {
            "nombre": candidato.nombre,
            "votos": candidato.votos,
            "porcentaje": round(porcentaje, 2)
        }

    # Transformación inmutable usando map
    return list(map(calcular_porcentaje, candidatos))

def graficar_resultados(candidatos: List[Candidato]) -> None:
    """Genera un gráfico de barras con los resultados actuales usando Matplotlib."""
    # Usamos map para extraer listas independientes sin usar bucles for
    nombres = list(map(lambda c: c.nombre, candidatos))
    votos = list(map(lambda c: c.votos, candidatos))

    if sum(votos) == 0:
        print("\n[Aviso] Aún no hay votos registrados para graficar.")
        return

    # Configuración del gráfico
    plt.figure(figsize=(10, 6))
    bars = plt.bar(nombres, votos, color=['#4C72B0', '#55A868', '#C44E52'])
    
    plt.title('Resultados Oficiales de las Elecciones', fontsize=14, fontweight='bold')
    plt.xlabel('Candidatos', fontsize=12)
    plt.ylabel('Cantidad de Votos', fontsize=12)
    
    # Añadir los números de votos encima de cada barra
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', va='bottom')

    plt.tight_layout()
    plt.show()