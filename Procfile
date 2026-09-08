web: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
worker: celery -A app.tasks.worker.celery_app worker --loglevel=info