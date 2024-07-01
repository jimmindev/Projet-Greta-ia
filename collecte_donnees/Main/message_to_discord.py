# main.py
import requests

def send_message_to_discord(message):
    webhook_url = "https://discordapp.com/api/webhooks/"  # Remplacez ceci par l'URL du webhook que vous avez copié
    data = {"content": message}

    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        print("message envoyé avec succès")
    else:
        print(f"Échec de l'envoi du message. Code d'état : {response.status_code}")
