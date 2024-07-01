##########################   TU : Savoir écrire dans un fichier texte en python   ###########################
#   Bonus Perso :                                                                                           #
#   Ajouter un log txt qui ajoute avec un ID les fichier log json                                           #
#   Le fichier Log Json contiendra le projet demandé + le retour de GPT                                     #
#############################################################################################################
import json
import os

########################################## LOG JSON ##########################################
def save_to_log_json(le_j,prompt):
    # Chemin vers le fichier JSON
    from datetime import datetime
    promt_temp = prompt.replace(' ', '_').replace('\'', '_').replace('.', '_').replace(',', '_')
    # Création d'une chaîne de date au format YYYY-MM-DD
    date_du_jour = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Remplacement des espaces et apostrophes par des underscores dans la demande
    nom_fichier_log = rf"{date_du_jour}_{promt_temp}.json"

    # Chemin vers le dossier
    chemin_dossier = "log_json"

    # Vérifier si le dossier existe
    if not os.path.exists(chemin_dossier):
        # Si le dossier n'existe pas, le créer
        os.makedirs(chemin_dossier)

    # Enregistrement du dictionnaire dans le fichier JSON
    with open("log_json/" + nom_fichier_log, 'w') as fichier_json:
        json.dump(le_j, fichier_json , indent=2)

    save_to_log_txt(nom_fichier_log)

def load_to_log_json(chemin_fichier_json):
    # Chemin vers le fichier JSON
    chemin_fichier_json = "log.json"
    mon_dictionnaire_charge = {}
    # Chargement du contenu du fichier JSON dans un dictionnaire
    with open(chemin_fichier_json, 'r') as fichier_json:
        mon_dictionnaire_charge = json.load(fichier_json)
    print(mon_dictionnaire_charge)


########################################## LOG TxT ##########################################
def save_to_log_txt(nom_fichier_log):
    nom_fichier_log_txt = "logs.txt"

    with open(nom_fichier_log_txt, 'a' ,  encoding='utf-8') as fichier_log_txt:
        fichier_log_txt.write(f"{nom_fichier_log}\n")

    print(f"Le nom du fichier log a été ajouté à {nom_fichier_log_txt}")


## Fonction pour Test

def test_():
    prompt = "Recette de tartiflette aux cerises soupoudré de cannelle et cuite au feu de bois"
    datas = {
    "Etape 1": {
        "titre": "Préparation des pommes de terre",
        "description": "Pelez et coupez les pommes de terre en rondelles de 5 mm d'épaisseur et rincez-les à l'eau froide.",
        "détail": "Si vous avez des pommes de terre nouvelles, vous pouvez les cuire à l'eau salée pendant 12 minutes avant de les couper. Cela permettra de diminuer le temps de cuisson de la tartiflette."
    },
    "Etape 2": {
        "titre": "Préparation des cerises",
        "description": "Dénoyautez les cerises et réservez-les dans un bol.",
        "détail": "Veillez à utiliser des cerises bien mûres et sucrées pour apporter une touche sucrée à la tartiflette. Vous pouvez également remplacer les cerises par d'autres fruits comme les framboises, les fraises ou les mûres."  
    },
    "Etape 3": {
        "titre": "Préparation de l'appareil à la crème",
        "description": "Dans un bol, mélangez la crème fraîche, les œufs, une pincée de sel et de poivre.",
        "détail": "Si vous êtes intolérant au lactose, vous pouvez remplacer la crème fraîche par de la crème végétale à base de soja ou d'amande. Vous pouvez également ajouter du fromage râpé dans l'appareil à la crème pour plus de saveurs."
    },
    "Etape 4": {
        "titre": "Montage de la tartiflette",
        "description": "Dans un plat à gratin, disposez une couche de pommes de terre, une couche de cerises et une couche de lardons fumés.",
        "détail": "Si vous êtes végétarien, vous pouvez remplacer les lardons fumés par des champignons ou du tofu fumé. Vous pouvez également ajouter des oignons émincés pour plus de goût."
    },
    "Etape 5": {
        "titre": "Répétition du montage",
        "description": "Répétez l'opération jusqu'à épuisement des ingrédients et terminez par une couche de pommes de terre.",
        "détail": "Veillez à bien tasser chaque couche pour que la tartiflette ne s'affaisse pas à la cuisson. Vous pouvez également ajouter des fines herbes pour apporter une touche de fraîcheur."
    },
    "Etape 6": {
        "titre": "Verser l'appareil à la crème",
        "description": "Versez l'appareil à la crème sur la tartiflette.",
        "détail": "Veillez à ce que l'appareil à la crème recouvre bien toute la tartiflette et qu'il y ait un espace entre l'appareil à la crème et le bord du plat pour éviter les débordements."
    },
    "Etape 7": {
        "titre": "Cuisson de la tartiflette",
        "description": "Faites cuire la tartiflette au feu de bois pendant environ 45 minutes.",
        "détail": "Il est important de vérifier la cuisson de la tartiflette en piquant les pommes de terre avec un couteau. Si les pommes de terre sont tendres, la tartiflette est prête."
    },
    "Etape 8": {
        "titre": "Finalisation de la cuisson",
        "description": "Soupoudrez la tartiflette de cannelle avant de la faire cuire 5 minutes supplémentaires.",
        "détail": "La cannelle apportera une note sucrée et épicée à la tartiflette. Vous pouvez également ajouter une pincée de noix de muscade pour plus de saveurs."
    },
    "Etape 9": {
        "titre": "Service de la tartiflette",
        "description": "Servez la tartiflette bien chaude accompagnée d'une salade verte.",
        "détail": "La tartiflette peut être accompagnée d'un verre de vin blanc de Savoie ou d'un cidre brut. Bon appétit !"
    },
    "Etape 10": {
        "titre": "Conservation de la tartiflette",
        "description": "La tartiflette se conserve au réfrigérateur pendant 2 à 3 jours.",
        "détail": "Pour réchauffer la tartiflette, vous pouvez la passer au four à 180°C pendant 10 à 15 minutes. Vous pouvez également la réchauffer au micro-ondes en la protégeant avec un couvercle ou un film alimentaire pour éviter que les bords ne sèchent."
        }
    }

    save_to_log_json(datas,prompt)
    load_to_log_json("log.json")