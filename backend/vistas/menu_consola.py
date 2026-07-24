"""Vista de consola (Paradigma Estructurado): menú, iteraciones y manejo de excepciones."""

import os
from servicios.sistema_electoral import SistemaElectoral
import servicios.analitica as analitica

def limpiar_pantalla():
    """Limpia la terminal, sea Windows (cls) o Unix (clear)."""
    os.system('cls' if os.name == 'nt' else 'clear')

def ejecutar_menu_votacion(sistema: SistemaElectoral):
    """Bucle principal del menú: votar o ver resultados, hasta que el usuario salga."""
    while True:
        limpiar_pantalla()
        print("=========================================")
        print("      SISTEMA ELECTORAL DIGITAL V2.0     ")
        print("=========================================")
        print("1. Ingresar al Módulo de Votación")
        print("2. Ver Reporte de Resultados (Matplotlib)")
        print("3. Salir del Sistema")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- IDENTIFICACIÓN DEL ELECTOR ---")
            dni = input("Ingrese su DNI (8 dígitos): ").strip()
            fecha_nacimiento = input("Ingrese su fecha de nacimiento (AAAA-MM-DD): ").strip()

            try:
                sistema.auth_service.verificar_identidad(dni, fecha_nacimiento)

                limpiar_pantalla()
                print("=========================================")
                print("            CANDIDATOS DISPONIBLES       ")
                print("=========================================")
                for id_cand, cand in sistema.candidatos.items():
                    print(f"[{id_cand}] {cand.nombre} - {cand.partido}")
                print("=========================================")

                seleccion = input("\nIngrese el número de su opción: ").strip()

                # input() siempre devuelve str: se valida a mano que sea un entero antes de convertir.
                if not seleccion.isdigit():
                    raise TypeError("La selección debe ser un número entero.")

                sistema.registrar_voto(dni, int(seleccion))
                print("\n[ÉXITO] ¡Su voto ha sido registrado correctamente!")
                input("\nPresione Enter para continuar...")

            # Manejo estructurado de errores
            except ValueError as ve:
                print(f"\n[ERROR] {ve}")
                input("Presione Enter para continuar...")
            except PermissionError as pe:
                print(f"\n[DENEGADO] {pe}")
                input("Presione Enter para continuar...")
            except TypeError as te:
                print(f"\n[FORMATO INVÁLIDO] {te}")
                input("Presione Enter para continuar...")
            except KeyError as ke:
                print(f"\n[OPCIÓN INVÁLIDA] {ke}")
                input("Presione Enter para continuar...")

        elif opcion == "2":
            limpiar_pantalla()
            print("=========================================")
            print("         REPORTE DE RESULTADOS           ")
            print("=========================================")
            try:
                # Extraemos la lista de objetos de nuestro diccionario
                lista_candidatos = list(sistema.candidatos.values())

                # 1. Reporte en texto (Paradigma Funcional)
                reporte = analitica.generar_reporte_porcentajes(lista_candidatos)
                total = analitica.calcular_total_votos(lista_candidatos)

                print(f"Total de Votos Emitidos: {total}\n")
                for item in reporte:
                    print(f"-> {item['nombre']}: {item['votos']} votos ({item['porcentaje']}%)")

                # 2. Generar el gráfico (Matplotlib)
                print("\nAbriendo gráfico interactivo...")
                analitica.graficar_resultados(lista_candidatos)

            except Exception as e:
                print(f"\n[ERROR] No se pudo generar el reporte: {e}")

            input("\nPresione Enter para volver al menú principal...")

        elif opcion == "3":
            print("\nCerrando sistema de forma segura...")
            break
        else:
            print("\nOpción no válida.")
            input("Presione Enter para continuar...")
