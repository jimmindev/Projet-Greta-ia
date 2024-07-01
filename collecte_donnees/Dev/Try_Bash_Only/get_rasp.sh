#!/bin/bash
url_page_php="http://192.168.20.183/modulesGrove.php?all"

recuperer_informations() {
    # Envoie de la requête HTTP pour récupérer les données de la page PHP
    reponse=$(curl -s "$1")

    # Vérification du code de statut de la réponse
    if [ $? -eq 0 ]; then
        # Analyse du contenu JSON
        donnees_json=$(echo "$reponse" | jq -c '.')
        
        # Retourne les données sous forme de JSON
        echo "$donnees_json"
    else
        # Affiche un message d'erreur si la requête échoue
        echo "Erreur: Impossible de récupérer les données."
        return 1
    fi
}

# Appel de la fonction pour récupérer les informations
informations=$(recuperer_informations "$url_page_php")

# Vérification si des informations ont été récupérées avec succès
if [ $? -eq 0 ]; then
    # Affichage des données récupérées
    echo "Données récupérées avec succès sur API Rasp:"
    echo "$informations" | while read -r key value; do
        echo "$key $value"
    done
else
    # 1 = erreur API rasp
    code_erreur=1
    bash gestion_erreurs.sh "$code_erreur"
fi