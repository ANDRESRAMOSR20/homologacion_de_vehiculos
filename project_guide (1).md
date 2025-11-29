# ✅ GUÍA COMPLETA PARA GENERACIÓN AUTOMÁTICA DEL PROYECTO  
### Python + FastAPI + IA + FAISS + Embeddings + LLM  
### **Archivo: project_guide.md**

---

# 🧱 Objetivo del Proyecto

Construir un servicio backend en **Python + FastAPI**, con IA, capaz de homologar nombres de vehículos proporcionados por partners con el catálogo oficial de Crabi.

El sistema debe usar:

- Normalización de texto  
- Embeddings semánticos (SentenceTransformers)  
- Buscador vectorial FAISS  
- LLM para desempate  
- Threshold configurable  
- Migraciones Alembic  
- API REST  
- Docker  

Este archivo describe **exactamente** qué debe ir en cada archivo

---


# 📌 CONTENIDO QUE DEBE IR EN CADA ARCHIVO

## 🟦 src/api/

### server.py
- Crear una instancia FastAPI  
- Cargar routers  
- Configurar CORS  
- Cargar settings desde .env  
- Levantar la aplicación  

### routers/matching_router.py
- Definir rutas: `POST /match`, `POST /match/batch`  
- Conectar con controlador  

### controllers/matching_controller.py
- Recibir request  
- Llamar matching_engine  
- Retornar respuesta  

---

# 🟩 src/core/matching/

### embedding_service.py
- Cargar SentenceTransformers  
- Generar embeddings  
- Cacheo  

### similarity_service.py
- Cargar FAISS  
- cosine similarity  
- top-k search  

### llm_service.py
- Cliente LLM  
- resolve_conflict()  

### matching_engine.py
Pipeline completo:
1. Normalizar  
2. Embedding  
3. FAISS top-k  
4. Threshold  
5. LLM si es necesario  
6. Retornar resultado  

---

# 🟧 src/core/normalization/

### normalizer.py
- lower  
- dedupe  
- expandir sinónimos  
- regex limpiar ruido  

### synonyms_map.py
Diccionario de equivalencias  

---

# 🟨 src/core/config/

### settings.py
Variables:
- DB_URL  
- MODEL_NAME  
- LLM_PROVIDER  
- SIM_THRESHOLD  
- VECTOR_INDEX_PATH  

### logger.py
- logging JSON  

---

# 🟫 src/core/db/

### database.py
- SQLAlchemy engine  
- SessionLocal  
- Base declarativa  

### models/vehicle.py
Modelo:
id, name

### migrations/001_seed_vehicles.py
Cargar catálogo inicial.
estos datos vienen de un archivo csv
---

# 🟪 src/vector_store/

### build_index.py
- Generar FAISS  
- Guardar index y cache  

---

# 🟥 src/schemas/

### match_request.py
partner_id, vehicle_name

### match_response.py
match, vehicle_id, confidence, llm_used

---

# 🟫 src/utils/

### text_utils.py
- remove_accents  
- dedupe_words  

### metrics.py
- métricas de similitud  

---

# 📘 tests/
- test_matching  
- test_normalization  
- test_api  

---

# 🐳 docker/

### Dockerfile
- python slim  
- uvicorn  

### docker-compose.yml
Servicios backend + DB

---

# 📜 scripts/

### init_db.py
Crear tablas

### load_catalog.py
Insertar catálogo

### build_vector_index.py
Construir FAISS

---

# 📦 requirements.txt
```
fastapi
uvicorn
sqlalchemy
alembic
python-dotenv
sentence-transformers
faiss-cpu
pydantic
requests
```

---

# 🚀 Indicaciones finales
1. Crear estructura EXACTA  
2. Generar código funcional  
3. Ejecutar con: `docker-compose up --build`  
4. FAISS con: `python scripts/build_vector_index.py`  
5. API final:  
   - POST /match  
   - POST /match/batch  

---

# ✔ FIN DEL ARCHIVO
