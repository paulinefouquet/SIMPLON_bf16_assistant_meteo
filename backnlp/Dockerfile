# Utiliser une image Python officielle comme base
FROM python:3.11-alpine

# Installer le client PostgreSQL
RUN apk add --no-cache postgresql-client

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le contenu actuel du répertoire vers le répertoire /app dans le conteneur
COPY . .

# #variables d'environnement
ENV DB_NAME 'postgres'
ENV USER 'postgres'
ENV PASSWORD 'pauline'
# ENV HOST 'host.docker.internal'
ENV DB_HOST 'postgres-pauline.h5cva6e4cthch7a2.westeurope.azurecontainer.io'
ENV PORT '5432'

# Installer les dépendances de l'application
RUN pip install --no-cache-dir fastapi uvicorn requests psycopg2-binary

# Exposer le port 8000
EXPOSE 8000

# Définir la commande à exécuter lors du démarrage du conteneur
CMD ["uvicorn", "nlp_api:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]