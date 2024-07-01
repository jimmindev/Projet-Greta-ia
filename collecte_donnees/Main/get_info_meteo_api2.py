# -*- coding: utf-8 -*-
import openmeteo_requests
import requests_cache
#import pandas as pd
from retry_requests import retry

import message_to_discord
import gestion_erreurs

import mysql.connector

def get_info_api_meteofull(Timezone):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 47.2488,
        "longitude": 6.0182,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "pressure_msl", "surface_pressure", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
        "hourly": "temperature_2m"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    if response is None:
        #  3: "Erreur API meteo !"
        log = gestion_erreurs.gerer_erreur(3)
        message_to_discord.send_message_to_discord(log)
        return None

    Coordinates_E = response.Latitude()
    Coordinates_N = response.Longitude()
    Elevation = response.Elevation()  # Elevation m asl
    #Timezone = response.Timezone()
    Timezone_difference = response.UtcOffsetSeconds()  # Timezone difference to GMT+0 s


    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_apparent_temperature = current.Variables(2).Value()
    current_is_day = current.Variables(3).Value()
    current_precipitation = current.Variables(4).Value()
    current_rain = current.Variables(5).Value()
    current_showers = current.Variables(6).Value()
    current_snowfall = current.Variables(7).Value()
    current_weather_code = current.Variables(8).Value()
    current_cloud_cover = current.Variables(9).Value()
    current_pressure_msl = current.Variables(10).Value()
    current_surface_pressure = current.Variables(11).Value()
    current_wind_speed_10m = current.Variables(12).Value()
    current_wind_direction_10m = current.Variables(13).Value()
    current_wind_gusts_10m = current.Variables(14).Value()
    

    if 1 == 2 :
        print(f"Current Coordinates_E {type(Coordinates_E)}")
        print(f"Current Coordinates_N {type(Coordinates_N)} ")
        print(f"Current Elevation {type(Elevation)} ")
        print(f"Current Timezone {type(Timezone)}")
        print(f"Current Timezone_difference {type(Timezone_difference)}")

        print(f"Current temperature_2m {type(current_temperature_2m)}")
        print(f"Current relative_humidity_2m {type(current_relative_humidity_2m)}")
        print(f"Current apparent_temperature {type(current_apparent_temperature)}")
        print(f"Current is_day {type(current_is_day)}")
        print(f"Current precipitation {type(current_precipitation)}")
        print(f"Current rain {type(current_rain)}")
        print(f"Current showers {type(current_showers)}")
        print(f"Current snowfall {type(current_snowfall)}")
        print(f"Current weather_code {type(current_weather_code)}")
        print(f"Current cloud_cover {type(current_cloud_cover)}")
        print(f"Current pressure_msl {type(current_pressure_msl)}")
        print(f"Current surface_pressure {type(current_surface_pressure)}")
        print(f"Current wind_speed_10m {type(current_wind_speed_10m)}")
        print(f"Current wind_direction_10m {type(current_wind_direction_10m)}")
        print(f"Current wind_gusts_10m {type(current_wind_gusts_10m)}")

    # Informations de connexion à la base de données
    config = {
        'user': 'jimmy',
        'password': 'jimmy',
        'host': '192.168.20.24',  # ou l'adresse IP du serveur MariaDB
        'database': 'collecte_donnees',  # Remplacez par le nom de votre base de données
        'raise_on_warnings': True
    }

    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        # Exécution de la requête INSERT
        cursor.execute("INSERT INTO Full_API_Meteo (Coordinates_E, Coordinates_N, Elevation, Timezone,  temperature_2m, relative_humidity_2m, apparent_temperature, is_day, precipitation, rain, showers, snowfall, weather_code, cloud_cover, pressure_msl, surface_pressure, wind_speed_10m, wind_direction_10m, wind_gusts_10m) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
    (Coordinates_E, Coordinates_N, Elevation, Timezone, current_temperature_2m, current_relative_humidity_2m, current_apparent_temperature, current_is_day, current_precipitation, current_rain, current_showers, current_snowfall, current_weather_code, current_cloud_cover, current_pressure_msl, current_surface_pressure, current_wind_speed_10m, current_wind_direction_10m, current_wind_gusts_10m))
        
        # Valider la transaction
        conn.commit()
    except mysql.connector.Error as err:
        # 4: "Erreur API meteo Insertion SQL !"
        log = gestion_erreurs.gerer_erreur(4)
        message_to_discord.send_message_to_discord(log)
    finally:
        # Fermeture de la connexion
        if conn.is_connected():
            cursor.close()
            conn.close()


    text = "API Meteo" + "\n"
    text = text + (f"Current Timezone {(Timezone)}") + "\n"
    text = text + (f"Current Coordinates_E {(Coordinates_E)}") + "\n"
    text = text + (f"Current Coordinates_N {(Coordinates_N)} ") + "\n"
    text = text + (f"Current Elevation {(Elevation)} ") + "\n"
    text = text + (f"Current Timezone_difference {(Timezone_difference)}") + "\n"

    text = text + (f"Current temperature_2m {(current_temperature_2m)}") + "\n"
    text = text + (f"Current relative_humidity_2m {(current_relative_humidity_2m)}") + "\n"
    text = text + (f"Current apparent_temperature {(current_apparent_temperature)}") + "\n"
    text = text + (f"Current is_day {(current_is_day)}") + "\n"
    text = text + (f"Current precipitation {(current_precipitation)}") + "\n"
    text = text + (f"Current rain {(current_rain)}") + "\n"
    text = text + (f"Current showers {(current_showers)}") + "\n"
    text = text + (f"Current snowfall {(current_snowfall)}") + "\n"
    text = text + (f"Current weather_code {(current_weather_code)}") + "\n"
    text = text + (f"Current cloud_cover {(current_cloud_cover)}") + "\n"
    text = text + (f"Current pressure_msl {(current_pressure_msl)}") + "\n"
    text = text + (f"Current surface_pressure {(current_surface_pressure)}") + "\n"
    text = text + (f"Current wind_speed_10m {(current_wind_speed_10m)}") + "\n"
    text = text + (f"Current wind_direction_10m {(current_wind_direction_10m)}") + "\n"
    text = text + (f"Current wind_gusts_10m {(current_wind_gusts_10m)}") + "\n"
    return text