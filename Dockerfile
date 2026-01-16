# Image de base légère
FROM python:3.11-slim

# Optimisations Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Définit le port par défaut pour que Streamlit sache quoi utiliser
ENV PORT 8080

WORKDIR /app

# Installation des dépendances (vérifiez que streamlit, pandas et google-generativeai y sont)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de tout le projet
COPY . .

# Cloud Run ignore EXPOSE, mais c'est une bonne pratique de doc
EXPOSE 8080

# Commande de lancement unique au format JSON (plus stable)
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8080", "--server.address=0.0.0.0"]