# FastAPI MDC Logger

A production-ready **FastAPI** project demonstrating **MDC (Mapped Diagnostic Context) style logging** using **Python standard logging** and `contextvars`.

This setup:

* Works with **FastAPI lifespan** (no deprecated APIs)
* Is **async-safe**
* Prints logs to **both terminal and file**
* Automatically injects `request_id` and `user_id` into every log message
* Uses **plain logging** (no JSON logger dependency)

---

## 📁 Project Structure

```
fastapi-mdc-logger/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── health.py
│   ├── core/
│   │   ├── logging.py
│   │   └── middleware.py
│   └── utils/
│       └── mdc.py
│
├── logs/
│   └── app.log
│
├── pyproject.toml
└── README.md
```

---

## 🚀 Features

* ✅ Async-safe MDC using `contextvars`
* ✅ `request_id` & `user_id` automatically added to logs
* ✅ Logs printed to **terminal + rotating file**
* ✅ Clean, readable log format
* ✅ FastAPI **lifespan** based startup/shutdown
* ✅ Compatible with `uv` package manager

---

## 🧠 What is MDC?

**Mapped Diagnostic Context (MDC)** allows you to attach contextual information (like `request_id`) to logs **without passing it manually** in every log call.

Equivalent to:

* Java: `SLF4J MDC`
* Python: `contextvars + logging`

---

## 📦 Requirements

* Python **3.10+**
* `uv` (recommended) or `pip install -r requirements.txt`

---

## ⚙️ Installation (using `uv`)

```bash
uv sync --all
```

This installs:

* FastAPI
* Uvicorn
* Dev tools (black, ruff, pytest)

---

## ▶️ Run the Application

```bash
uv run uvicorn app.main:app --reload
or
uvicorn app.main:app --reload
```

Open in browser:

```
http://127.0.0.1:8000/health
```

---

## 🧪 Sample API

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

## 🪵 Sample Log Output

### Terminal / File (`logs/app.log`)

```
2025-12-23 22:26:11 INFO app.api.health [request_id=91b3e9fa user_id=anonymous] Health check endpoint called
```

No manual string formatting required in business code:

```python
logger.info("Health check endpoint called")
```

---

## 🔗 MDC Flow

1. **Middleware** generates or reads `X-Request-ID`
2. Values stored in `contextvars`
3. Custom `LogRecordFactory` injects MDC into log message
4. Handlers print logs to console + file

---

## 🛠️ Logging Design Highlights

* Uses **RotatingFileHandler** (10MB, 5 backups)
* Prevents duplicate logs during reload
* Safe for async / concurrent requests
* No external logging dependencies

---

## 🧩 Configuration Files

* `app/core/logging.py` → logging + MDC injection
* `app/core/middleware.py` → request context setup
* `app/utils/mdc.py` → MDC storage using `contextvars`

---

## 🚧 Startup & Shutdown Logs

Uses FastAPI **lifespan** (recommended approach):

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application started")
    yield
    logger.info("Application shutting down")
```

Startup logs won’t have `request_id` (no request context) — this is expected.

---

## 👨‍💻 Author

**Janardhan Singh**
Backend / Platform Engineer

---

## 📄 License

MIT License
