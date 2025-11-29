# 🚗 Sistema de Homologación de Vehículos con IA

Este documento detalla la arquitectura, tecnologías y decisiones de diseño implementadas para el sistema de homologación de vehículos.

## 🛠️ Stack Tecnológico

### 1. Backend: **Python + FastAPI**
*   **Justificación**: Python es el estándar de facto para IA y procesamiento de datos. FastAPI se eligió por su alto rendimiento (asíncrono), validación automática de datos (Pydantic) y generación automática de documentación (Swagger UI).
*   **Uso**: Manejo de la API REST, orquestación de servicios y lógica de negocio.

### 2. Base de Datos: **SQLite + SQLAlchemy**
*   **Justificación**: Para este MVP, SQLite ofrece simplicidad (sin servidor) y portabilidad. SQLAlchemy (ORM) permite abstraer las consultas SQL, facilitando la migración futura a PostgreSQL o MySQL sin cambiar el código.
*   **Uso**: Almacenamiento del catálogo oficial (`vehicles`) y vehículos de socios (`partner_vehicles`).

### 3. Búsqueda Vectorial: **FAISS (Facebook AI Similarity Search)**
*   **Justificación**: FAISS es una librería altamente optimizada para búsqueda de similitud en vectores densos. Es mucho más eficiente que comparar embeddings uno por uno (fuerza bruta), permitiendo escalar a millones de registros.
*   **Uso**: Indexación de los embeddings de los nombres de vehículos oficiales para recuperación rápida de candidatos (Top-K).

### 4. Embeddings: **SentenceTransformers (all-MiniLM-L6-v2)**
*   **Justificación**: Este modelo es un equilibrio perfecto entre velocidad y precisión semántica. Genera vectores de 384 dimensiones que capturan el significado del texto, permitiendo encontrar "Mazda 3" aunque se escriba "Mazda3" o "Mzda 3".
*   **Uso**: Conversión de descripciones de texto a vectores numéricos.

### 5. LLM: **OpenAI GPT-4o-mini**
*   **Justificación**: A pesar de la búsqueda vectorial, existen casos ambiguos (ej. "Mazda 3" vs "Mazdaspeed 3"). Un LLM tiene el "sentido común" automotriz para distinguir versiones deportivas, años o errores tipográficos graves que los vectores no captan.
*   **Uso**: Desempate inteligente cuando la confianza de la búsqueda vectorial es media o hay múltiples candidatos muy cercanos.

### 6. Contenedorización: **Docker & Docker Compose**
*   **Justificación**: Garantiza que el entorno de ejecución sea idéntico en desarrollo y producción, eliminando problemas de dependencias ("en mi máquina funciona").
*   **Uso**: Empaquetado de la aplicación y sus librerías.

### 7. IDE: **Antigravity**
*   **Justificación**: La nueva herramienta de google mostro innovacion con la nueva herramienta Agent Manager la cual sirve de guiador para esquematizar el desarrollo, llevandose a cursor con gran diferencia.
*   **Uso**: Esquematizar y realizar montajes de una forma mas facil y estructurada, ademas de un markdowm de guia en cada una de sus inferencias.
---

## 🚧 Desafíos y Soluciones

### 1. El Problema de "Mazdaspeed3"
*   **Desafío**: El sistema no emparejaba "Mazda Mazdaspeed3" con "Mazda 3".
*   **Análisis**: Vectorialmente son similares, pero conceptualmente son vehículos distintos (versión deportiva vs estándar).
*   **Solución**: El LLM actuó correctamente al rechazar el match. Esto validó que el sistema es robusto ante falsos positivos peligrosos.

### 2. Consultas Cortas vs Descripciones Largas
*   **Desafío**: Una búsqueda como "Mazda 3" tenía baja similitud vectorial con "MAZDA MAZDA3 2008 I TOURING..." debido a la diferencia de longitud y palabras extra.
*   **Solución**: Implementamos **Búsqueda Híbrida**.
    *   Combinamos el puntaje vectorial (semántico) con un puntaje de **Token Overlap** (Jaccard/Intersección).
    *   Fórmula: `Score Final = 0.6 * Vector + 0.4 * Overlap`.
    *   Esto priorizó los resultados que contenían las palabras exactas de la búsqueda.

### 3. Contexto del LLM
*   **Desafío**: Inicialmente, el LLM recibía solo IDs (ej. "M-100") y no podía decidir.
*   **Solución**: Modificamos el `SimilarityService` para devolver tuplas `(id, nombre, score)` y actualizamos el prompt del LLM para incluir los nombres completos de los candidatos.


## 📂 Estructura del Proyecto

### `src/api/`
*   **`server.py`**: Punto de entrada de la aplicación FastAPI.
*   **`controllers/`**: Lógica de negocio que conecta la API con los servicios.
*   **`routers/`**: Definición de endpoints HTTP (`/match`, `/metrics`).

### `src/core/matching/`
*   **`matching_engine.py`**: Orquestador principal. Coordina normalización -> embedding -> búsqueda -> LLM.
*   **`similarity_service.py`**: Maneja el índice FAISS y la lógica de búsqueda híbrida.
*   **`llm_service.py`**: Cliente de OpenAI para resolución de conflictos.
*   **`embedding_service.py`**: Generación de vectores con SentenceTransformers.

### `src/core/normalization/`
*   **`normalizer.py`**: Limpieza de texto, eliminación de acentos y expansión de sinónimos (ej. "VW" -> "VOLKSWAGEN").

### `src/core/db/`
*   **`models/`**: Definición de tablas (`Vehicle`, `PartnerVehicle`).
*   **`migrations/`**: Scripts para carga inicial de datos (`seed_vehicles.py`).

### `scripts/`
*   **`process_partner_vehicles.py`**: Script batch para procesar masivamente vehículos de socios.
*   **`build_vector_index.py`**: Genera el índice FAISS a partir de la base de datos.
*   **`manual_match.py`**: Herramienta para forzar emparejamientos manualmente.

---

## 🚀 Flujo de "Catálogo Unificado"

El sistema implementa una lógica de auto-aprendizaje para vehículos no encontrados:

1.  Se busca el vehículo en el **Catálogo Oficial**.
2.  Si hay match -> Se asigna el ID oficial.
3.  Si **NO** hay match -> El sistema **crea automáticamente** una nueva entrada en el catálogo con un ID propio (`SOC-XXX`).
4.  Se reconstruye el índice vectorial para que este nuevo vehículo sea "encontrable" en el futuro.

Esto permite que el catálogo crezca orgánicamente con la información de los socios, manteniendo la integridad de los datos oficiales.

---

## 📖 Manual de Usuario

### 1. Despliegue Local
Una vez que el contenedor Docker está corriendo (`docker-compose up`), la API estará disponible en:

👉 **http://localhost:8000**

*   **Documentación Interactiva (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
*   **Métricas de Uso**: [http://localhost:8000/match/metrics](http://localhost:8000/match/metrics)

### 2. Probando el Sistema
Puedes probar la homologación enviando una petición POST a `/match/`.

<p align= "center"> <img width="781" height="476" alt="prueba-api" src="https://github.com/user-attachments/assets/d809dd64-5acd-4eb5-a9b7-a26e3076c752" /></p>


**Ejemplo de Request (JSON):**
```json
{
  "partner_id": "SOCIO-123",
  "vehicle_name": "Mazda 3 2008 Touring"
}
```

**Ejemplo de Respuesta (JSON):**
```json
{
  "match": true,
  "vehicle_id": "M-100",
  "confidence": 0.92,
  "llm_used": false
}
```

### 3. Scripts de Utilidad
Para ejecutar tareas administrativas dentro del contenedor:

*   **Cargar Catálogo Oficial**:
    ```bash
    docker-compose exec api python src/core/db/migrations/versions/001_seed_vehicles.py
    ```
*   **Cargar Vehículos de Socios**:
    ```bash
    docker-compose exec api python src/core/db/migrations/versions/002_seed_partner_vehicles.py
    ```
*   **Procesamiento Batch (Catálogo Unificado)**:
    ```bash
    docker-compose exec api python scripts/process_partner_vehicles.py
    ```
*   **Reconstruir Índice Vectorial**:
    ```bash
    docker-compose exec api python scripts/build_vector_index.py
    ```

### 4. Despliegue desde Docker Hub
Cualquier persona puede descargar y ejecutar la última versión del sistema directamente desde la nube:

1.  **Descargar la imagen**:
    ```bash
    docker pull klenstoner/homologacion_de_vehiculos-api
    ```

2.  **Ejecutar el contenedor**:
    Es necesario pasar la API Key de OpenAI como variable de entorno.
    ```bash
    docker run -p 8000:8000 -e OPENAI_API_KEY="tu-api-key-aqui" klenstoner/homologacion_de_vehiculos-api
    ```

3.  **Probar**:
    El servicio estará disponible en `http://localhost:8000`.





