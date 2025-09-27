FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Salin direktori 'app' ke dalam direktori kerja di container
COPY ./app .

EXPOSE 8000

# Perintah CMD diupdate untuk merujuk ke 'main:app' di dalam modul 'app'
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]