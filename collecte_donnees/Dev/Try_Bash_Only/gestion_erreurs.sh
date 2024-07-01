#!/bin/bash

gerer_erreur() {
    case $1 in
        1)
            echo "Erreur API rasp !"
            # Ajoutez ici le code pour gérer l'erreur API rasp
            ;;
        2)
            echo "Erreur API meteo !"
            # Ajoutez ici le code pour gérer l'erreur API meteo
            ;;
        3)
            echo "Erreur Insertion SQL !"
            # Ajoutez ici le code pour gérer l'erreur Insertion SQL
            ;;
        4)
            echo "Erreur Envoi Email !"
            # Ajoutez ici le code pour gérer l'erreur Envoi Email
            ;;
        *)
            echo "Erreur inconnue: Argument non valide"
            ;;
    esac
}

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <code_erreur>"
    exit 1
fi

code_erreur=$1
gerer_erreur "$code_erreur"