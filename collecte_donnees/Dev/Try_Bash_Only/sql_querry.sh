#!/bin/bash

# Informations de connexion à la base de données
user="jimmy"
password="jimmy"
host="192.168.20.24"
database="collecte_donnees"
horodatage="$1"  # Premier argument : horodatage
temperature_capteur="$2"  # Deuxième argument : temperature_capteur
humidite_capteur="$3"  # Troisième argument : humidite_capteur
temperature_donnerMeteo="$4"  # Quatrième argument : temperature_donnerMeteo
humidite_donnerMeteo="$5"  # Cinquième argument : humidite_donnerMeteo
rasp_id="$6"  # Sixième argument : rasp_id

# Exécution de la requête INSERT et capture du code de sortie
error_code=$(mysql -u "$user" -p"$password" -h "$host" -D "$database" --execute="INSERT INTO donnee (timestamp, temperature_ext, humidity_ext, temperature_int, humidity_int, raspi_id) VALUES ('$horodatage', $temperature_capteur, $humidite_capteur, $temperature_donnerMeteo, $humidite_donnerMeteo, $rasp_id);" 2>&1)

# Vérification du code de sortie
if [ $? -eq 0 ]; then
    echo "Insertion réussie"
else
    echo "Erreur lors de l'insertion : $error_code"
fi