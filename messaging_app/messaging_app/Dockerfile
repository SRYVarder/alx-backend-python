FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY requirements.txt /app/ || true
RUN apt-get update && apt-get install -y build-essential netcat && rm -rf /var/lib/apt/lists/* || true
RUN pip install --no-cache-dir django gunicorn || true
COPY . /app/
EXPOSE 8000
CMD ["gunicorn", "messaging_app.wsgi:application", "--bind", ":8000"]