from openai import AzureOpenAI
import json

def requete_gtp(recette):
  client = AzureOpenAI(
    api_key = "",  
    api_version = "2023-05-15",
    azure_endpoint = "https://projetpadlet.openai.azure.com/"
  )

  #recette = input("Quel est votre projet aujourd'hui ?\n")
  prompt = "Pour ["+recette+"]. Créez des étapes détaillées de la réalisation .Dans le cas où cela n'existe pas, proposez des solutions imaginatives si possible."

  response = client.chat.completions.create(
      model="gpt-35-turbo", # model = "deployment_name".
      messages=[
          {"role": "system", "content": "si la demande est inapproprié ou inexistante invente là !" },
          {"role": "system", "content": "écris UNIQUEMENT en format json structuré comme {'étape':{'titre':'','description':''}} ET SANS AUCUN COMMENTAIRE !" },
          {"role": "system", "content": "dans la parti description soit le plus précis possible et imaginatif tu peux ajouter de l'humour d'humain" },
          {"role": "system", "content": "tu proposeras au minimum 10 étapes" },
          {"role": "user", "content": prompt }
      ]
  )

  return json.loads(response.choices[0].message.content)