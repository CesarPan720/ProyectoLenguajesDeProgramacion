# 🗳️ Sistema Electoral Digital Multiparadigma

Este proyecto es una solución de software desarrollada en Python diseñada para gestionar un proceso de votación de manera segura, robusta y persistente. El sistema aplica una arquitectura modular que combina múltiples paradigmas de programación para resolver requerimientos específicos, y está preparado para una futura escalabilidad (como la integración de validación biométrica/reconocimiento facial).

## 🚀 Características Principales

* **Control de Padrón Electoral:** Validación estricta de votantes mediante DNI (Expresiones Regulares - RegEx).
* **Persistencia Atómica:** Guardado de votos y actualización del padrón en archivos `.json` mediante operaciones transaccionales seguras, evitando corrupción de datos ante cortes de energía.
* **Trazabilidad y Auditoría:** Registro de eventos críticos y errores en un archivo log (`logging`).
* **Analítica Visual:** Generación de reportes de porcentajes y gráficos estadísticos interactivos de los resultados en tiempo real.

## 🧠 Paradigmas de Programación Aplicados

El proyecto fue diseñado aplicando los siguientes paradigmas de forma justificada según el problema a resolver:

1. **Paradigma Orientado a Objetos (POO):** Utilizado en el modelado de datos (`Candidato`) y la gestión de responsabilidades (`ServicioAutenticacion`, `SistemaElectoral`). Permite el encapsulamiento de los estados (votos) y facilita la futura extensión del sistema sin romper el código existente (Principio Abierto/Cerrado).
   
2. **Paradigma Funcional:**
   Aplicado en el módulo de `analitica.py`. Se utilizan funciones puras de orden superior y cierres léxicos (`map`, `reduce`, `lambdas`) para transformar la información inmutable, calcular porcentajes y preparar los vectores de datos necesarios para la graficación estadística, evitando el uso de bucles convencionales.

3. **Paradigma Estructurado:**
   Implementado en las vistas (`menu_consola.py`) y en el flujo principal del controlador. Maneja las secuencias lógicas del menú, iteraciones (`while`) e implementa un control de flujo altamente robusto mediante bloques `try-except` para capturar excepciones específicas (`ValueError`, `PermissionError`, `TypeError`).

## 📂 Estructura del Proyecto

```text
proyecto_elecciones/
├── datos/                  # Base de datos JSON (Padrón y Resultados)
├── modelos/                # Entidades (POO)
│   └── candidato.py
├── servicios/              # Lógica de negocio y controladores
│   ├── analitica.py        # Procesamiento estadístico (Funcional)
│   ├── autenticacion.py    # Validación y seguridad (POO/Estructurado)
│   ├── gestor_archivos.py  # Persistencia atómica de E/S
│   └── sistema_electoral.py# Controlador principal
├── vistas/                 # Interfaz de usuario
│   └── menu_consola.py     # Menú y manejo de excepciones
├── main.py                 # Punto de entrada de la aplicación
├── .gitignore              # Reglas de exclusión de Git
└── README.md               # Documentación del proyecto