# API Flask MySQL CRUD avec Authentification JWT
Ceci est une simple application Flask qui fournit des opérations CRUD (Créer, Lire, Mettre à jour, Supprimer) pour une base de données MySQL. Elle inclut également l'authentification JSON Web Token (JWT) pour sécuriser les points de terminaison de l'API.

## Prérequis
```
Python 3.x
Flask
mysql-connector-python
jwt
```
Vous pouvez installer les paquets requis en utilisant pip :
pip install Flask mysql-connector-python jwt


## Configuration
Remplacez les valeurs suivantes dans le code par votre clé secrète et les détails de connexion à la base de données :

```
SECRET_KEY = 'azerty123qsdfgh456'
db_config = {
    'host': '192.168.20.24',
    'user': 'jimmy',
    'password': 'jimmy',
    'database': 'Test_API'
}
```

## Utilisation
Exécutez l'application Flask :
``` 
python app.py 
```

L'API sera disponible à l'adresse http://192.168.20.24:5000.

## Points de terminaison
- GET ```/select/<table>``` : Récupère tous les enregistrements de la table spécifiée. Nécessite un jeton JWT valide.
- POST ```/insert/<table>``` : Insère un nouvel enregistrement dans la table spécifiée. Nécessite un jeton JWT valide.
- PUT ```/update/<table>/<id>``` : Met à jour l'enregistrement avec l'ID spécifié dans la table spécifiée. Nécessite un jeton JWT valide.
- DELETE ```/delete/<table>/<id>``` : Supprime l'enregistrement avec l'ID spécifié de la table spécifiée. Nécessite un jeton JWT valide.
- GET ```/get_token/<login>/<password>``` : Génère un jeton JWT pour les identifiants d'utilisateur spécifiés.

## Middleware
Le middleware token_required est utilisé pour vérifier et décoder le jeton JWT dans les en-têtes de la requête.  
Si le jeton est manquant, expiré ou invalide, le middleware renverra une réponse d'erreur appropriée.

## Gestion des erreurs
L'application inclut une gestion des erreurs de base pour les opérations de base de données et le décodage du jeton JWT. \
Si une erreur inattendue se produit, le serveur renverra une réponse d'erreur 500 avec un message.

## Sécurité
Les jetons JWT sont utilisés pour l'authentification.
Le middleware token_required vérifie la présence et la validité du jeton JWT dans les en-têtes de la requête.
Le point de terminaison generate_token2 valide les informations d'identification de l'utilisateur et génère un jeton JWT avec une date d'expiration.
Le middleware token_required décode le jeton JWT et vérifie le rôle de l'utilisateur pour l'autorisation.
