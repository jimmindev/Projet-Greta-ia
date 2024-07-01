#######################   TU : Savoir utiliser l'API padlet pour créer un post   ########################
#       Fournir le code python qui permet de créer un post sur Padlet (avec des données de test)        #
#########################################################################################################

import requests
import json

## TU Envoi Padlet + TU JSON  = TI Envoi Padlet avec un Json
def api_padlet(Padlet_ID,API_KEY , Tab_ID , titre , contenu , url ):
    payload = {
        "data": {
            "type": "post",
            "attributes": {
                "content": {
                    "subject": titre,
                    "body": contenu
                }
            },
            "relationships": {
                "section": {
                    "data": {
                        "id": Tab_ID
                    }
                }
            }
        }
    }
    
    headers = {
        "accept": "application/vnd.api+json",
        "content-type": "application/json",
        "X-Api-Key": API_KEY
    }
    response = requests.post(url, data=json.dumps(payload) , headers=headers)
    #print(response.text)



## TU Envoi Padlet
def test_():
    Padlet_ID = "v96n8l3kxjayrndm"
    API_KEY = ""
    Tab_ID = "sec_mVbpvYpBKPjLqRkn"
    url = "https://api.padlet.dev/v1/boards/"+Padlet_ID+"/posts"
    titre = input("Entrer le titre pour le padlet : ")
    contenu = input("Entrer le contenu pour le padlet : ")
    api_padlet(Padlet_ID,API_KEY , Tab_ID , titre , contenu , url )

# test_()