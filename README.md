# meteo

## Chargement des données de l'API meteoFrance

Toutes les 3H ce service charge les données de forecast de MétéoFrance et supprime les datas anciennes de plus de 30H

### Démarrage :

Construire une image à partir du backend/Dockerfile
Executer le container

## Microservice meteo -> text et audio

API nlp qui fait appel à edenai

### Obtenir une key

### Démarrage :

Construire une image à partir du backnlp/Dockerfile
Executer le container sur le port 8000
```
drun -p 8000:8000 <nom de l'image générée>
```

## Démarrer d'un serveur front-end sur le port 8001

Exécutez la commande suivante à la racine du projet
```
python -m http.server 8001
```

Rendez-vous sur la page http://localhost:8001/frontend/