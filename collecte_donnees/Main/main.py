# -*- coding: utf-8 -*-
import time
from datetime import datetime
import get_info_ras
import get_info_meteo_api2
import message_to_discord


def main():
    timestamp = datetime.fromtimestamp(time.time())
    text = ""
    #Recuperation des info Raspberry
    text = text + get_info_ras.get_info_rasp(timestamp,"192.168.20.181") #Rasp 1
    text = text + get_info_ras.get_info_rasp(timestamp,"192.168.20.182") #Rasp 2
    text = text + get_info_ras.get_info_rasp(timestamp,"192.168.20.183") #Rasp 3

    #Recuperation des info API Meteo
    text = text + get_info_meteo_api2.get_info_api_meteofull(timestamp)

    message_to_discord.send_message_to_discord(text)

if __name__ == "__main__":
    main()