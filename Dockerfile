FROM python:3.12-slim

WORKDIR /app

# Copie et install des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY app/ ./app/

# Variables d'environnement
ENV NASA_API_KEY=KrVBixAMRPibikKOBY0OdymP7O2AQh2IfwKDFBZh
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
