import pandas as pd

chemin_fichier_csv = 'adresse.csv'

def get_random_adresse():
    donnees = pd.read_csv(chemin_fichier_csv, sep=';')
    colonnes_selectionnees = donnees[['numero', 'voie_nom', 'commune_nom', 'long', 'lat']]
    #print(colonnes_selectionnees)
    ligne_aleatoire = colonnes_selectionnees.sample().reset_index(drop=True)
    
    # Affichez la ligne aléatoire et accédez à la valeur de la colonne "numero"
    #print(ligne_aleatoire)
    #print(ligne_aleatoire["numero"].iloc[0])  # Accéder à la valeur de "numero" dans la ligne aléatoire
    
    return ligne_aleatoire

get_random_adresse()

