# 🗳️ Sistema Electoral Digital Multiparadigma

Este proyecto es una solución de software desarrollada en Python diseñada para gestionar un proceso de votación de manera segura, robusta y persistente. El sistema aplica una arquitectura modular que combina múltiples paradigmas de programación para resolver requerimientos específicos. El backend expone tanto un menú de consola como una API REST (FastAPI), consumida por un frontend web (Vue 3 + Tailwind).

## 🚀 Características Principales

* **Control de Padrón Electoral:** Validación estricta de votantes mediante DNI (Expresiones Regulares - RegEx).
* **Persistencia en MySQL:** Lectura y escritura de candidatos y padrón electoral mediante consultas y transacciones seguras (con rollback automático ante errores), evitando corrupción de datos.
* **Trazabilidad y Auditoría:** Registro de eventos críticos y errores en un archivo log (`logging`).
* **Analítica Visual:** Generación de reportes de porcentajes y gráficos estadísticos interactivos de los resultados en tiempo real.
* **Dos formas de uso:** menú de consola interactivo (demostración de los paradigmas) y una API REST + interfaz web para votar desde el navegador.

## 🧠 Paradigmas de Programación Aplicados

El proyecto fue diseñado aplicando los siguientes paradigmas de forma justificada según el problema a resolver:

1. **Paradigma Orientado a Objetos (POO):** Utilizado en el modelado de datos (`Candidato`) y la gestión de responsabilidades (`ServicioAutenticacion`, `SistemaElectoral`, `GestorBaseDatos`). Permite el encapsulamiento de los estados (votos) y facilita la futura extensión del sistema sin romper el código existente (Principio Abierto/Cerrado).

2. **Paradigma Funcional:**
   Aplicado en el módulo de `analitica.py`. Se utilizan funciones puras de orden superior y cierres léxicos (`map`, `reduce`, `lambdas`) para transformar la información inmutable, calcular porcentajes y preparar los vectores de datos necesarios para la graficación estadística, evitando el uso de bucles convencionales.

3. **Paradigma Estructurado:**
   Implementado en las vistas (`menu_consola.py`) y en el flujo principal del controlador. Maneja las secuencias lógicas del menú, iteraciones (`while`) e implementa un control de flujo altamente robusto mediante bloques `try-except` para capturar excepciones específicas (`ValueError`, `PermissionError`, `TypeError`, `KeyError`).

## 🗄️ Persistencia de Datos

El sistema usa MySQL (ver `database/base.sql`) con dos tablas:

* `padron_electoral(dni, votado, biometria_registrada)`: controla quién puede votar y si ya lo hizo.
* `candidatos(id_candidato, nombre, partido, votos)`: candidatos disponibles y su conteo de votos (incluye la opción "Voto en Blanco" como una fila más).

Toda la conexión y las consultas/transacciones pasan por `GestorBaseDatos` (`backend/servicios/gestor_base_datos.py`), que centraliza el manejo de errores de conexión (`RuntimeError`) y hace `commit`/`rollback` explícito en cada transacción.

## 📂 Estructura del Proyecto

```text
ProyectoLenguajesDeProgramacion/
├── backend/
│   ├── modelos/
│   │   └── candidato.py         # Entidad Candidato (POO)
│   ├── servicios/
│   │   ├── analitica.py         # Procesamiento estadístico (Funcional)
│   │   ├── autenticacion.py     # Validación de identidad por DNI (POO/Estructurado)
│   │   ├── gestor_base_datos.py # Conexión y transacciones MySQL (POO)
│   │   └── sistema_electoral.py # Controlador principal (POO)
│   ├── vistas/
│   │   └── menu_consola.py      # Menú de consola y manejo de excepciones (Estructurado)
│   ├── api.py                   # API REST (FastAPI) sobre los mismos servicios
│   ├── esquemas.py               # Esquemas Pydantic de la API
│   ├── main.py                   # Punto de entrada del menú de consola
│   └── requirements.txt          # Dependencias de Python
├── frontend/                     # Interfaz web (Vue 3 + Tailwind CSS)
│   └── src/
│       ├── views/                # LoginView, VotingView, ResultsView
│       ├── stores/               # Estado (Pinia): auth, candidatos
│       └── services/             # Llamadas a la API REST
├── database/
│   └── base.sql                  # Esquema y datos iniciales de MySQL
├── docker/
│   ├── Dockerfile.backend        # Imagen de la API (uvicorn)
│   └── Dockerfile.frontend       # Imagen del frontend (Vite dev server)
├── docker-compose.yml            # Orquesta MySQL, phpMyAdmin, backend y frontend
├── .env                          # Variables de entorno (no versionado)
├── .gitignore
└── README.md
```

## 🌐 API REST

El backend expone estos endpoints (ver `backend/api.py`), consumidos por el frontend:

| Método | Ruta | Descripción | Errores mapeados |
|---|---|---|---|
| GET | `/api/health` | Chequeo de disponibilidad | — |
| POST | `/api/auth/verificar` | Verifica que el DNI exista en el padrón y no haya votado | 400 formato inválido, 403 no registrado / ya votó |
| GET | `/api/candidatos` | Lista de candidatos (incluye "Voto en Blanco") | — |
| POST | `/api/votos` | Registra el voto de un DNI para un candidato | 400, 403, 404 candidato inválido |
| GET | `/api/resultados` | Total de votos y porcentaje por candidato | — |

## 🖥️ Frontend

Aplicación Vue 3 + Vite + Tailwind CSS con tres pantallas principales: identificación por DNI (`LoginView`), selección y confirmación del voto (`VotingView`), y reporte de resultados (`ResultsView`). Consume la API REST anterior mediante `axios` y mantiene el estado de sesión/candidatos con Pinia.

## 🐳 Ejecución con Docker (recomendado)

Con un archivo `.env` en la raíz (variables de MySQL, puertos de backend/frontend), levantar todo con:

```bash
docker-compose up -d
```

Esto levanta MySQL (con el esquema de `database/base.sql` ya cargado), phpMyAdmin, la API (FastAPI/uvicorn) y el frontend (Vite). Luego solo hay que abrir `http://localhost:<FRONTEND_PORT_HOST>` en el navegador.

El menú de consola (`main.py`) sigue disponible dentro del contenedor del backend, para la demostración del paradigma estructurado:

```bash
docker exec -it sistemaElectoral_backend python main.py
```

## ⚙️ Ejecución local sin Docker (opcional)

```bash
cd backend
pip install -r requirements.txt
python main.py              # Menú de consola
# o bien:
uvicorn api:app --reload    # API REST en http://localhost:8000
```

Requiere una instancia de MySQL accesible y las variables `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` configuradas en el entorno.
