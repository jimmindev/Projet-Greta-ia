import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from appli import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_ok_button_clicked)
        self.pushButton_2.clicked.connect(self.on_push_button_2_clicked)
        
        self.ui.pushButton_close_windows.clicked.connect(lambda:
            self.showMinimized())
        
        
    def on_ok_button_clicked(self):
        # Logique pour le bouton OK
        nom_cave = self.nom_caveLineEdit.text()
        adresse_cave = self.adresse_caveLineEdit.text()
        code_cave = self.code_caveLineEdit.text()
        email_cave = self.email_caveLineEdit.text()
        self.textEdit.append(f"Nom: {nom_cave}, Adresse: {adresse_cave}, Code: {code_cave}, Email: {email_cave}")
        
    def on_push_button_2_clicked(self):
        # Logique pour le deuxième bouton
        self.label_2.setText("Le texte a été changé!")  # Changer le texte du label
        self.textEdit.append("PushButton clicked!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())