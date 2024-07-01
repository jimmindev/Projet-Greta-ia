# Collecte de données météorologiques et domotiques

## Cahier des charges
Une collectivité fait un appel à projet pour doter son bâtiment d'une gestion thermique intelligente. 

Votre équipe de développeur IA répond à l'appel à projet et déploie la première étape : collecter les données thermiques du bâtiment (température, humidité, présence, etc.) ainsi que les données météorologiques (temporelles et prédictives). 

Vous mettrez en place un système qui permet de réaliser cette collecte en différents points du bâtiment avec une collecte toutes les heures et un horodatage de chaque nouvelle entrée. 

Votre application devra alerter l'administrateur en cas de dysfonctionnement de l'application en sachant d'où vient le problème (BDD, ou un des deux points de collecte). 

Un système de Log doit être prévu pour avoir un historique de chaque dysfonctionnement. 



# Main Collecte
Ce script récupère des informations depuis des Raspberry Pi et une API météorologique, puis envoie les données à Discord.

```
def main():
    # Récupère des informations depuis des Raspberry Pi
    # Récupère des informations depuis une API météorologique
    # Envoie les données à Discord
```
# Script get_info_ras
Ce script récupère des données depuis des Raspberry Pi, les traite, et les stocke dans une base de données. Il gère également les erreurs et envoie des messages à Discord.

```
def get_info_rasp(Timezone , rasp_ip ):
    # Arguments:
    #   Timezone: la zone temporelle actuelle
    #   rasp_ip: l'adresse IP du Raspberry Pi
    # Renvoie:
    #   Une chaîne de caractères contenant les informations récupérées
```
# Script get_info_meteo_api2
Ce script récupère des données météorologiques depuis une API, les traite, et les stocke dans une base de données. Il gère également les erreurs et envoie des messages à Discord.

```
def get_info_api_meteofull(Timezone):
    # Argument:
    #   Timezone: la zone temporelle actuelle
    # Renvoie:
    #   Une chaîne de caractères contenant les informations météorologiques récupérées
```
# Script message_to_discord
Ce script envoie un message à un webhook Discord.

```
def send_message_to_discord(message):
    # Argument:
    #   message: le message à envoyer
```
Cette description se concentre sur les fonctions principales de chaque script, en expliquant les arguments qu'elles prennent et ce qu'elles renvoient.