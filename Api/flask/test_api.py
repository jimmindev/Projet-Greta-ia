import requests

##################################################
#               Doc en bas de page !!!           #
##################################################


# URL de base de votre API
BASE_URL = 'http://192.168.20.24:5000'
YOUR_TOKEN = "" # Reste Vide !!!

def get_token(login , password):
    url = f'{BASE_URL}/get_token/{login}/{password}'
    response = requests.get(url)
    return response.json()


# account-type  : "login" , "mdp" 
# user : "jeremy" , "jeremy"
# admin(unlimited time token) : "jimmy" , "jimmy"

# Generation du Token
login    = "jeremy"  # Mettre Login  !!!!!!!!!!!!!!!
password = "jeremy"  # Mettre Mdp    !!!!!!!!!!!!!!!
response = get_token(login , password )

# Ensure response is a dictionary
if isinstance(response, dict):
    if 'token' in response and response['token']:
        YOUR_TOKEN = response['token']
        print("[LOG] Token =", YOUR_TOKEN)
    elif 'error' in response:
        print(f"[ERROR] Authentication failed: {response['error']}")
        exit()
    else:
        print("[ERROR] Unexpected response format")
        exit()
else:
    print(f"[ERROR] Unexpected response type: {type(response)}")
    exit()
    

# Exemple de sélection (Read)
def select_data(table):
    global YOUR_TOKEN
    url = f'{BASE_URL}/select/{table}'
    headers = {'Authorization': YOUR_TOKEN}
    response = requests.get(url, headers=headers)
    print(response.json())
    return response.json()


# Exemple d'insertion (Create)
def insert_data(table, data):
    global YOUR_TOKEN
    url = f'{BASE_URL}/insert/{table}'
    headers = {'Content-Type': 'application/json', 'Authorization': YOUR_TOKEN}
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    return response.json()


# Exemple de mise à jour (Update)
def update_data(table,data,id):
    global YOUR_TOKEN
    url = f'{BASE_URL}/update/{table}/{id}'  # Remplacez 1 par l'ID de la ligne que vous souhaitez mettre à jour
    headers = {'Content-Type': 'application/json', 'Authorization': YOUR_TOKEN}
    response = requests.put(url, json=data, headers=headers)
    print(response.json())
    return response.json()

# Exemple de suppression (Delete)
def delete_data(table, id):
    global YOUR_TOKEN
    url = f'{BASE_URL}/delete/{table}/{id}'  # Remplacez 1 par l'ID de la ligne que vous souhaitez supprimer
    headers = {'Authorization': YOUR_TOKEN}
    response = requests.delete(url, headers=headers)
    print(response.json())
    return response.json()

#############################################################
#                       accounts                            #
#############################################################
#         Nom	            Type                            #
#         id                Primaire	int(11)             #
#         user	            varchar(50)                     #
#         password	        varchar(50)                     #
#         expiration	    date                            #
#         roles	            int(1)                          #
#############################################################

#############################################################
#                       donnees                             #
#############################################################
#         Nom	            Type                            #
#         id                Primaire	int(11)             #
#         Temp	            float                           #
#         Hum	            float                           #
#         Rasp_id	        nt(11)	                        #
#############################################################

# Exécutez les exemples
if 1 == 1 :
    select_data("accounts;delete from donnees where id = 4 ;") #Select et afficher la table "accounts"

# Appel de la fonction d'insertion
if 1 == 2 :
    table_name = 'donnees'  # Nom de la Table
    data_to_insert = {'Temp': '-50.0', 'Hum': '12.5' , 'Rasp_id' : '1'} # Clé = Nom colonne , valeur = Valeur a mettre
    insert_data(table_name, data_to_insert)

#Select pour vérification
if 1 == 2 :
    select_data("donnees")

#Fonction Update
if 1 == 2 :
    table_name = 'donnees'  # Nom de la Table
    data_to_insert = {'Temp': '100000000'}  # Clé = Nom colonne : valeur = Valeur a mettre
    update_data(table_name, data_to_insert,4)

#Fonction Update
if 1 == 2 :
    table_name = 'donnees'  # Nom de la Table
    id = 1 # Id de la ligne a supprimer
    delete_data(table_name, id )