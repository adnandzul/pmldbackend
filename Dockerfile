# Dockerfile BARU (Benar)

FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app /code/app

EXPOSE 4000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]