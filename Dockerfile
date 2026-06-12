FROM python:3.12-slim

WORKDIR /app

COPY sample_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY sample_service .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
