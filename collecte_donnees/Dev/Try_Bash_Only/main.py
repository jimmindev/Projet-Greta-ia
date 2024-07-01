# -*- coding: utf-8 -*-
import time
from datetime import datetime
import get_info_ras
import get_info_meteo_api
import sql_querry
import gestion_erreurs
import message_to_discord

def main():
    #Recuperation des info Raspberry
    temperature_ras, humidite_ras = get_info_ras.get_info_rasp()
    try :
        temperature_ras = float(temperature_ras)
        humidite_ras    = float(humidite_ras)
    except :
        # 1 = erreur API rasp
        log = gestion_erreurs.gerer_erreur(1)
        message_to_discord.send_message_to_discord(log)
        return None

    #Recuperation des info API Meteo
    temperature_api, humidite_api = get_info_meteo_api.get_info_api_meteo()
    try :
        temperature_api = float(temperature_api)
        humidite_api    = float(humidite_api)
    except :
        # 2 = erreur API meteo
        log = gestion_erreurs.gerer_erreur(2)
        message_to_discord.send_message_to_discord(log)
        return None

    #Envoi Information Rasp + Api en dataSql
    timestamp = datetime.fromtimestamp(time.time())
    try :
        rasp_id = 3
        sql_querry.insert_sql(timestamp,temperature_ras,humidite_ras,temperature_api,humidite_api,rasp_id)
        message_to_discord.send_message_to_discord(f"Raspberry ({rasp_id}): \nTemperature : {temperature_ras}\nhumidite{temperature_ras}\n\nAPI Meteo :\nTemperature : {temperature_api}\nhumidite{humidite_api}")
    except :
        # 2 = erreur API meteo
        log = gestion_erreurs.gerer_erreur(3)
        message_to_discord.send_message_to_discord(log)
        return None

 
if __name__ == "__main__":
    main()