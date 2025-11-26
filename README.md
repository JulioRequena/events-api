# Events API - Proyecto técnico (FastAPI)

Proyecto mínimo para correr localmente una API REST para registrar y consultar eventos.

## Contenido
- `app/` - código de la aplicación (FastAPI)
- `Dockerfile` - imagen multi-stage
- `requirements.txt` - dependencias
- `.gitlab-ci.yml` - pipeline de CI/CD (ejemplo)
- `k8s/` - manifiestos Kubernetes
- `grafana/dashboard-events.json` - dashboard mínimo para Grafana
- `sonar-project.properties` - SonarQube settings
- `tests/` - tests pytest básicos

## Ejecutar localmente (sin Docker)
1. Crear y activar un entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate    # Windows (PowerShell)
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar la API:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
4. Endpoints:
   - POST http://localhost:8000/api/v1/events
   - GET  http://localhost:8000/api/v1/events
   - GET  http://localhost:8000/api/v1/events/{id}
5. Métricas Prometheus:
   - http://localhost:8001/metrics

## Ejecutar con Docker (local)
1. Build:
   ```bash
   docker build -t events-api:local .
   ```
2. Run:
   ```bash
   docker run -p 8000:8000 -p 8001:8001 events-api:local
   ```

## Ejecutar tests
```bash
pytest -q
```

## Notas
- Esto es un proyecto de referencia; en producción debe añadirse DB (Postgres), migraciones (Alembic),
  autenticación, y ajustes de seguridad.


Levantar la aplicación con Docker (local)
✅ 1. Descomprime el proyecto
Descomprime el archivo:
events-api.zip
Deberías ver esta estructura:
events-api/
 ├── app/
 ├── tests/
 ├── Dockerfile
 ├── requirements.txt
 ├── sonar-project.properties
 ├── .gitlab-ci.yml
 ├── k8s/
 └── README.md
________________________________________
✅ 2. Construir la imagen Docker
Desde la carpeta raíz del proyecto:
docker build -t events-api:local .
Esto hace:
•	Instala dependencias.
•	Copia el código.
•	Expone el puerto 8000.
•	Configura uvicorn como servidor.
________________________________________
✅ 3. Ejecutar el contenedor
docker run -d \
  -p 8000:8000 \
  -p 8001:8001 \
  --name events-api \
  events-api:local
Esto expone:
Servicio	Puerto Local
API REST	8000
/metrics Prometheus	8001
________________________________________
✅ 4. Verificar que está corriendo
✔ Ver logs
docker logs -f events-api
✔ Probar endpoint principal
curl http://localhost:8000/health
Debe responder:
{"status": "ok"}
________________________________________
🍀 5. Usar la API desde el navegador
📌 Documentación interactiva (Swagger/OpenAPI)
👉 Abre en el navegador:
http://localhost:8000/docs
📌 Lista de eventos
GET http://localhost:8000/events
________________________________________
📊 6. Métricas
Para ver las métricas estilo Prometheus:
http://localhost:8001/metrics
Estas serán usadas luego por Grafana/Prometheus en Kubernetes.
________________________________________
🧹 7. Detener y eliminar
docker stop events-api
docker rm events-api

