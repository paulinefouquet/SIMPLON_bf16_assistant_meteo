# meteo

Executer le container postgres sur Azure

depuis le repertoire postgres/  
```
dbt my-postgres-image .
```

depuis le repertoire backend/  
```
dbt load-data-azure .
```

depuis le repertoire backnlp/  
```
dbt image-nlp-azure .
```

```
docker tag load-data-azure apimeteonlp.azurecr.io/pauline-load-data-azure
docker push apimeteonlp.azurecr.io/pauline-load-data-azure
docker tag image-nlp-azure apimeteonlp.azurecr.io/pauline-api-nlp-azure
docker push apimeteonlp.azurecr.io/pauline-api-nlp-azure
```

## Prérequis:
Avoir installé postgres en local, avoir défini un password et démarré le serveur:  
DB_NAME 'postgres'  
USER 'postgres'  
PASSWORD 'pauline'  
HOST 'localhost'  
PORT '5432'  

démarrer Docker desktop  

## Chargement des données de l'API meteoFrance

Toutes les 3H ce service charge les données de forecast de MétéoFrance et supprime les datas anciennes de plus de 30H  

### Démarrage :

Construire une image à partir dans le répertoire backend/  
```
docker build -t mateo-back .
```
Executer le container  
```
docker run mateo-back
```

## Microservice meteo -> text et audio

API qui fait appel à edenai pour générer du texte et un audio

### Obtenir une Key de EdenAI

https://docs.edenai.co/reference/start-your-ai-journey-with-edenai  

Dans répertoire backnlp, créer un fichier dupliquer le fichier config.py.example et le renommer config.py y modifier la variable avec la clé obtenue auprès de edenai  
EDENAI_KEY = "Bearer xxxxxxxxxxxxxx....xxxxxxxxxxxxxxxxxxx"

### Démarrage :

Construire une image docker dans le répertoire backnlp/
```
docker build -t <nom de l'image> .
```
Executer le container sur le port 8000
```
docker run -p 8000:8000 <nom de l'image>
```

## Démarrer d'un serveur front-end sur le port 8001

Exécutez la commande suivante à la racine du projet
```
python -m http.server 8001
```

Rendez-vous sur la page http://localhost:8001/frontend/