# Image de base légère
FROM python:3.11-slim

# Empêche Python de générer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Installation des dépendances
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code et des données
COPY . .

# Port exposé par Cloud Run (8080 par défaut)
EXPOSE 8080

# Commande de lancement (ici pour FastAPI)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]

CMD streamlit run frontend/app.py --server.port=8080 --server.address=0.0.0.0