# Project001 — (Nginx Reverse Proxy + FastAPI) 🐳
 Simple **multi-container Docker Compose** project: **Nginx** sits in front as a **reverse proxy** and routes `/api/*` requests to a **Python FastAPI** backend. The backend also writes lightweight request logs into a **Docker named volume**.

---

## What it does

- **Nginx**
  - Serves a static homepage on `/`
  - Health check on `/health` → returns `ok`
  - Reverse proxy routes `/api/*` → FastAPI service

- **FastAPI**
  - `/api/health` → API health status
  - `/api/inspect` → shows request info (headers/IP/user-agent) and appends a line to a log file

---

## Why reverse proxy?

A **reverse proxy** is a server that receives requests from clients and forwards them to backend services.

Client → **Nginx (reverse proxy)** → **FastAPI (backend)**

Benefits:
- One public entrypoint (only Nginx is exposed)
- Backend stays private inside Docker network
- Easy routing (`/api/*`), security rules, caching later

---

## Project structure

```
Project001/
  docker-compose.yml
  nginx/
    default.conf
  app/
    Dockerfile
    requirements.txt
    main.py
  site/
    index.html
```

---

## Run

From inside `Project001/`:

### PowerShell / CMD
```bash
docker compose up --build
```

Open:
- http://localhost:8080
- http://localhost:8080/health
- http://localhost:8080/api/health
- http://localhost:8080/api/inspect

Stop:
```bash
docker compose down
```

---

## View API logs (saved in volume)

```bash
docker exec -it edgeprobe-api sh -c "tail -n 50 /logs/requests.log"
```

---

## Troubleshooting

### Port already in use
Edit `docker-compose.yml` and change:
```yaml
ports:
  - "8080:80"
```
to:
```yaml
ports:
  - "8081:80"
```
Then run again:
```bash
docker compose up --build
```

### Nginx shows 502 Bad Gateway
Check containers and logs:
```bash
docker compose ps
docker logs edgeprobe-nginx
docker logs edgeprobe-api
```

---

## today practiced - 14-01-2026

- Docker images vs containers
- Port mapping (`-p HOST:CONTAINER`)
- Docker Compose multi-container apps
- Container networking (service-name DNS: `api:8000`)
- Nginx reverse proxy routing
- Named volumes for persistent logs
```
