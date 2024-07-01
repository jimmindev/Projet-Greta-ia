# -*- coding: utf-8 -*-
def send_message_to_bot(queue, message):
    queue.put(message)


def gerer_erreur(argument):
    error_message = ""
    error_messages = {
        1: "Erreur API rasp !",
        2: "Erreur API rasp Insertion SQL !",
        3: "Erreur API meteo !",
        4: "Erreur API meteo Insertion SQL !",
        5: "Erreur Envoi Email !" ,
        6: "Erreur inconnue: Argument non valide"
    }

    if argument in error_messages:
        error_message = error_messages[argument]
        print(error_message)

        # Enregistrement de l'erreur dans le fichier log.txt
        log_file_path = "log.txt"
        with open(log_file_path, "a") as log_file:
            log_file.write(f"{error_message}\n")

    else:
        error_message = error_messages[5]
        print("Erreur inconnue: Argument non valide")
        # Ajoutez ici le code pour gérer l'erreur inconnue

        # Enregistrement de l'erreur dans le fichier log.txt
        log_file_path = "log.txt"
        with open(log_file_path, "a") as log_file:
            log_file.write(f"Erreur inconnue: Argument non valide ({argument})\n")
    
    return error_message