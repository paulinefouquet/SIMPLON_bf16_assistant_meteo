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
#ENV HOST 'host.docker.internal'
ENV DB_HOST 'postgres-pauline.h5cva6e4cthch7a2.westeurope.azurecontainer.io'
ENV PORT '5432'

# Installer les dépendances de l'application
RUN pip install psycopg2-binary meteofrance_api tqdm schedule

# Définir la commande à exécuter lors du démarrage du conteneur
CMD ["python", "main.py"]