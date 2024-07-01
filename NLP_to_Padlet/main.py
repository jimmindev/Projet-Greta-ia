#Requete utilisateur
from TU_TI.Recuperer_le_souhait_de_l_utilisateur.Input_user import saisi_input
requete_user = saisi_input()
#print(requete_user)

#Requete utilisateur to ChatGpt Azure
from TU_TI.Extraire_les_bonnes_donnees_de_la_reponse_de_chat_GPT.Openai_Azure import requete_gtp
requete_gpt_user = requete_gtp(requete_user)
#print(requete_gpt_user)

#Log de la demande utilisateur et de la réponse chat gpt
from TU_TI.Savoir_ecrire_dans_un_fichier_texte_en_python.Log import save_to_log_json
save_to_log_json(requete_gpt_user , requete_user)

#Envoi dans la Section Padlet
from TU_TI.Savoir_utiliser_l_API_padlet_pour_creer_un_post.API_Padlet import api_padlet
#Configuraton du Padlet 
Padlet_ID = "v96n8l3kxjayrndm"
API_KEY = ""
Tab_ID = "sec_mVbpvYpBKPjLqRkn"
titre = " "
contenu = " "
url = "https://api.padlet.dev/v1/boards/"+Padlet_ID+"/posts"

for x in requete_gpt_user:
    titre = x + " : " +  requete_gpt_user[x]["titre"]
    contenu = requete_gpt_user[x]["description"]
    print(titre),print(contenu)
    api_padlet(Padlet_ID, API_KEY , Tab_ID , titre , contenu , url )