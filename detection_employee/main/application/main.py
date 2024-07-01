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
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Application\nAdministrateur", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Consultation LOG", command=self.view_log_file)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

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
        self.initial_label = customtkinter.CTkLabel(self.centered_frame, text="Bienvenu dans l'application InsideFace !")
        self.initial_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def view_log_file(self):
        # remove existing content from the centered frame
        for widget in self.centered_frame.winfo_children():
            widget.destroy()

        # create a text box to display the contents of the log file
        self.log_text = customtkinter.CTkTextbox(self.centered_frame, wrap="none")
        self.log_text.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")

        # create a scrollbar for the text box
        self.scrollbar = customtkinter.CTkScrollbar(self.centered_frame, command=self.log_text.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # configure the text box to use the scrollbar
        self.log_text.configure(yscrollcommand=self.scrollbar.set)

        # create a progress bar to show the progress of reading the log file
        self.progress_bar = customtkinter.CTkProgressBar(self.centered_frame, orientation="horizontal", mode="determinate")
        self.progress_bar.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="nsew")
        self.progress_bar.set(0.1)

        # start the reading process in a separate thread
        threading.Thread(target=self.read_log_file_thread).start()

    def read_log_file_thread(self):
        # create an SSH connection
        conn = Connection(host=ip, user="jimmy", connect_kwargs={"password": "jimmy"})

        # read the contents of the log file
        result = conn.run("tail -n 200 ./projet/log.txt")

        # update the progress bar
        self.progress_bar.set(0.5)

        # insert the contents of the log file into the text box
        self.log_text.insert("end", result.stdout)

        # scroll to the end of the text box
        self.log_text.see("end")

        # update the progress bar
        self.progress_bar.set(1.0)

if __name__ == "__main__":
    app = App()
    app.create_initial_content()
    app.mainloop()
