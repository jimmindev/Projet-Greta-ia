import tkinter
import tkinter.messagebox
import tkcalendar

import customtkinter
from fabric import Connection
import os
import threading
import time
from datetime import datetime

import logging
import pandas as pd

import mysql.connector
from mysql.connector import Error


customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

ip = "192.168.207.128"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("insight-face")
        self.geometry("800x600")
        self.grid_columnconfigure(1, weight=1)  # set weight of column 1 to 1

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Application RH", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Formulaire Employé", command=self.open_form_content)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Exportation Excel", command=self.excel_export)
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)

        # create content frame
        self.content_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # create a frame to center the content
        self.centered_frame = customtkinter.CTkFrame(self.content_frame, corner_radius=0)
        self.centered_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.centered_frame.grid_rowconfigure(0, weight=1)
        self.centered_frame.grid_columnconfigure(0, weight=1)

        # create initial content
        self.create_initial_content()

    def create_initial_content(self):
        # create a label to display initial content
        self.initial_label = customtkinter.CTkLabel(self.centered_frame, text="Bienvenu dans l'application Inside Face !")
        self.initial_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def open_form_content(self):
        # remove existing content from the centered frame
        for widget in self.centered_frame.winfo_children():
            widget.destroy()

        # create form frame
        self.form_frame = customtkinter.CTkFrame(self.content_frame, corner_radius=0, fg_color="transparent")
        self.form_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.form_frame.columnconfigure(1, weight=1)  # set column 1 to take up all available space

        # create form labels and entries
        name_label = customtkinter.CTkLabel(self.form_frame, text="Nom : ")
        name_label.grid(row=0, column=0, sticky="w")
        name_entry = customtkinter.CTkEntry(self.form_frame)
        name_entry.grid(row=0, column=1, sticky="ew")

        last_name_label = customtkinter.CTkLabel(self.form_frame, text="Prénom : ")
        last_name_label.grid(row=1, column=0, sticky="w")
        last_name_entry = customtkinter.CTkEntry(self.form_frame)
        last_name_entry.grid(row=1, column=1, sticky="ew")

        # create a browse button to select the .mp4 file
        self.browse_button = customtkinter.CTkButton(self.form_frame, text="Parcourir", command=self.browse_file)
        self.browse_button.grid(row=2, column=0, padx=(10, 0), pady=10)

        # create a label to display the selected file path
        self.file_path_label = customtkinter.CTkLabel(self.form_frame, text="")
        self.file_path_label.grid(row=2, column=1, padx=(10, 0), pady=10, sticky="w")

        # create a submit button
        submit_button = customtkinter.CTkButton(self.form_frame, text="Valider", command=lambda: self.submit_form(name_entry.get(), last_name_entry.get()))
        submit_button.grid(row=3, column=1, padx=50, pady=10, sticky="nsew")

    def browse_file(self):
        # use a file dialog to let the user select a .mp4 file
        file_path = tkinter.filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])

        if file_path:
            # set the selected file path
            self.file_path = file_path
            # display the selected file path in the label
            self.file_path_label.configure(text=file_path)

    def submit_form(self, name, surname):
        # process form data
        print(f"Nom : {name}")
        print(f"Prenom : {surname}")
        print(f"filename : {self.file_path}" )

        # hide the form frame
        self.form_frame.grid_forget()

        # show the progress bar and loading message
        self.loading_label = customtkinter.CTkLabel(self.centered_frame, text="[1/4] Upload de la vidéo en cours...")
        self.loading_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        self.progress_bar = customtkinter.CTkProgressBar(self.centered_frame, orientation="horizontal", mode="determinate")
        self.progress_bar.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="nsew")
        self.progress_bar.set(0.1)

        # start the upload process in a separate thread
        threading.Thread(target=self.send_file_to_vm, args=(self.file_path, name , surname ) ).start()

    def send_file_to_vm(self, file_path , name , surname ):
        # Paramètres de connexion SSH
        conn = Connection(host= ip , user="jimmy", connect_kwargs={"password": "jimmy"})
        name_file = f"{name}_{surname}.mp4"
        print(name_file)
        # Envoi du fichier à l'aide de la commande put de Fabric
        conn.put(file_path, remote=f"projet/upload/{name_file}" )

        # Vérification que le fichier a bien été upload
        result = conn.run(f"ls projet/upload/{name_file}")
        
        remote_file_path = f"projet/upload/{name_file}"
        if remote_file_path in result.stdout:
            print("Le fichier a bien été upload.")
        else:
            print("Le fichier n'a pas été upload.")



        self.loading_label.configure(text="[2/4]  Detection visage de la vidéo en cours...")
        self.progress_bar.set(0.2)
        
        # Activation de l'environnement virtuel
        conn.run("source /home/jimmy/projet/.venv/bin/activate")
        
        # Exécution du script de détection du visage de la vidéo sur la machine virtuelle
        result = conn.run(f"/home/jimmy/projet/.venv/bin/python3 -c 'import sys; sys.path.append(\"projet\"); import video_crop_face; print(video_crop_face.video_crop(\"{remote_file_path}\"))'")
        return_code = int(result.stdout.strip().split("\n")[-1])
                
        if return_code == 1:
            print("Video crop OK")
        else:
            print("Video crop pas OK")



        self.loading_label.configure(text="[3/4]  Enregistrement dans la base de données ...")
        self.progress_bar.set(0.4)
        id_employer = connect_to_database(name , surname)
        if id_employer == 1:
            print("Insert SQL OK")
        else:
            print("Insert SQL No OK")
        
        self.loading_label.configure(text="[4/4]  Fabrication du Model ...")
        self.progress_bar.set(0.6)
        
        # Exécution du script de détection du visage de la vidéo sur la machine virtuelle
        result = conn.run(f"/home/jimmy/projet/.venv/bin/python3 -c 'import sys; sys.path.append(\"projet\"); import main_1_initialisation_dataset; print(main_1_initialisation_dataset.datasetinsert(\"{id_employer}\",\"{name}\",\"{surname}\"))'")
        return_code = int(result.stdout.strip().split("\n")[-1])
        if return_code == 1:
            print("Model OK")
        else:
            print("Model pas OK")
            
        self.employer_ok()


    def employer_ok(self):
        # remove existing content from the centered frame
        for widget in self.centered_frame.winfo_children():
            widget.destroy()
        self.emp_ok = customtkinter.CTkLabel(self.centered_frame, text="Enregistrement de l'employé avec succès")
        self.emp_ok.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def erreur(self):
        print(self)


    def excel_export(self):
        # remove existing content from the centered frame
        for widget in self.centered_frame.winfo_children():
            widget.destroy()

        # create form frame
        self.form_frame = customtkinter.CTkFrame(self.content_frame, corner_radius=0, fg_color="transparent")
        self.form_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.form_frame.columnconfigure(1, weight=1)  # set column 1 to take up all available space

        start_date_label = customtkinter.CTkLabel(self.form_frame, text="Date de début : ")
        start_date_label.grid(row=2, column=0, sticky="w")
        self.start_date_entry = tkcalendar.DateEntry(self.form_frame, date_pattern='yyyy-mm-dd')
        self.start_date_entry.grid(row=2, column=1, sticky="ew")

        end_date_label = customtkinter.CTkLabel(self.form_frame, text="Date de fin : ")
        end_date_label.grid(row=3, column=0, sticky="w")
        self.end_date_entry = tkcalendar.DateEntry(self.form_frame, date_pattern='yyyy-mm-dd')
        self.end_date_entry.grid(row=3, column=1, sticky="ew")

        # create a submit button
        submit_button = customtkinter.CTkButton(self.form_frame, text="Valider", command=lambda: self.submit_form_excel(self.start_date_entry.get(), self.end_date_entry.get()))
        submit_button.grid(row=4, column=1, padx=50, pady=10, sticky="nsew")
        
    def submit_form_excel(self,start_date_entry , end_date_entry):
        print(start_date_entry)
        print(end_date_entry)
        try:
            # Connexion à la base de données
            conn = mysql.connector.connect(
            host= ip ,
            database='Cam_Auto_Badge',
            user='jimmy',
            password='Ey4@WKIF!3lm)e*y'
        )
            cursor = conn.cursor(dictionary=True)

            # Requête pour obtenir les données de passage entre deux dates
            query = """
            SELECT p.id_passage, p.horaire_passage, p.entree_sortie_passage, e.id_employe, e.nom_employe, e.prenom_employe
            FROM Passages p
            JOIN Employes e ON p.id_employe = e.id_employe
            WHERE p.horaire_passage BETWEEN %s AND %s
            order by id_passage
            """
            cursor.execute(query, (start_date_entry, end_date_entry))
            passages = cursor.fetchall()

            # Fermer la connexion à la base de données
            cursor.close()
            conn.close()
        
            # Convertir les données en DataFrame pandas
            df = pd.DataFrame(passages)

            # Obtenir la date et l'heure actuelles pour le nom de fichier Excel
            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_file = f"./excel/passages_{current_datetime}.xlsx"
    
            # Créer le répertoire 'excel' s'il n'existe pas
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            # Exporter le DataFrame en fichier Excel
            df.to_excel(output_file, index=False)

        except mysql.connector.Error as err:
            logging.error(f"Erreur: {err}")
            return []


        
        
        
def connect_to_database(nom , prenom):
    try:
        # Établir la connexion à la base de données
        connection = mysql.connector.connect(
            host= ip ,
            database='Cam_Auto_Badge',
            user='jimmy',
            password='Ey4@WKIF!3lm)e*y'
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            cursor = connection.cursor()

            # Exécuter la requête SQL INSERT
            insert_query = "INSERT INTO Employes ( nom_employe, prenom_employe) VALUES ( %s, %s)"
            employee_data = ( nom , prenom )
            cursor.execute(insert_query, employee_data)
            connection.commit()  # Valider la transaction

            # Récupérer l'ID de l'employé nouvellement inséré
            employee_id = cursor.lastrowid
            print("Insertion réussie. ID de l'employé :", employee_id)
            return employee_id

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def get_passages(start_date, end_date):
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host= ip ,
            database='Cam_Auto_Badge',
            user='jimmy',
            password='Ey4@WKIF!3lm)e*y'
        )
        cursor = conn.cursor(dictionary=True)

        # Requête pour obtenir les données de passage entre deux dates
        query = """
        SELECT p.id_passage, p.horaire_passage, p.entree_sortie_passage, e.id_employe, e.nom_employe, e.prenom_employe
        FROM Passages p
        JOIN Employes e ON p.id_employe = e.id_employe
        WHERE p.horaire_passage BETWEEN %s AND %s
        """
        cursor.execute(query, (start_date, end_date))
        passages = cursor.fetchall()

        # Fermer la connexion à la base de données
        cursor.close()
        conn.close()

        return passages

    except mysql.connector.Error as err:
        logging.error(f"Erreur: {err}")
        return []


if __name__ == "__main__":
    app = App()
    app.mainloop()
