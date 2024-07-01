# Projet de détection de publicités avec IA et feu tricolore

Ce projet vise à développer une application capable de détecter automatiquement la présence de publicités sur un décodeur TV à l'aide d'une caméra IP et d'un modèle d'intelligence artificielle. L'application utilise un feu tricolore pour indiquer visuellement si une publicité est détectée et stocke les salves d'images détectées dans une base de données NoSQL Firebase. Une interface web dynamique avec React permet à l'administrateur de surveiller le flux télévisuel, de consulter les salves d'images et les rapports détaillés, et d'insérer de nouveaux échantillons pour les classes du modèle.

## Fonctions principales du programme

1. **Capture et analyse d'images en temps réel** : Le programme capture en continu des images du flux télévisuel à l'aide d'une caméra IP et les analyse à l'aide d'un modèle d'IA pour classer chaque séquence comme "PUB" ou "NoPub".
2. **Gestion des logs et des hyperparamètres** : Les salves d'images détectées sont stockées dans une base de données Firebase, accompagnées d'un fichier log contenant des informations telles que la durée de la salve, le nombre d'images, les hyperparamètres du modèle, l'horodatage, et les résultats de prédiction pour chaque image et la prédiction moyenne par classe.
3. **Interface web dynamique avec React** : L'interface web offre une vue en direct de la caméra IP, permettant à l'administrateur de surveiller le flux télévisuel. Elle permet également de consulter les salves d'images en fonction de la date et de l'heure, d'accéder aux rapports détaillés pour chaque salve sélectionnée, et d'insérer de nouveaux échantillons pour les classes du modèle ("PUB" et "NoPub").
4. **Communication avec le feu tricolore (simulateur décodeur)** : Des requêtes HTTP sont utilisées pour changer la couleur du feu tricolore selon les résultats de prédiction du modèle : vert pour une probabilité de "NoPub" supérieure à 70%, orange pour une probabilité entre 5% et 70% sur la classe majoritaire, et rouge pour une probabilité de "PUB" supérieure à 70%.
5. **Administration et notifications** : Le site web propose une connexion sécurisée pour l'administrateur et envoie des alertes par mail ou des notifications Push en cas de défaillance système (connexion BDD, API décodeur, caméra IP, modèle, etc.).

## Site
https://projetpub-a1920.web.app/home

