# Gym Analytics Management API

Backend API built with FastAPI, SQLAlchemy, SQLite, Pydantic, and pytest under a Spec Driven Development flow.

## Run locally

1. Create and activate virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the API:

```bash
uvicorn src.main:app --reload
```

4. Open docs:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## Run tests

```bash
pytest -q
```
