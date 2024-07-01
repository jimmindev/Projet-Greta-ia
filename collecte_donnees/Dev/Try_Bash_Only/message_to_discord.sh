#!/bin/bash

send_message_to_discord() {
    webhook_url="https://discordapp.com/api/webhooks/1186689063512715334/iVSKtsL716tQ1DAF51zxs8KPKZSVk9QgOYHx5gNJQg_WMHjZ6IHZmb5XEHxYJfr3u5eS"
    message="$1"
    data="{\"content\":\"$message\"}"

    response=$(curl -s -X POST -H "Content-Type: application/json" -d "$data" "$webhook_url")

    if [ $? -eq 0 ] && [ "$response" == "" ]; then
        echo "Message envoyé avec succès"
    else
        echo "Échec de l'envoi du message. Réponse : $response"
    fi
}

# Exemple d'utilisation
send_message_to_discord "$1"