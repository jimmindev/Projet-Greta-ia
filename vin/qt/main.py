import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtCore import Qt, QPoint
from appli import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Enlever la barre de titre
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)


        # Masquer body_right (si nécessaire)
        self.body_right.hide()

        # Variables pour suivre le déplacement de la fenêtre
        self.draggable = False
        self.offset = QPoint()

        # Control de la fenetre
        self.pushButton_reduce_windows.clicked.connect(lambda: self.showMinimized())
        self.pushButton_maxi_windows.clicked.connect(lambda: self.restore_or_maximize_window())
        self.pushButton_close_windows.clicked.connect(lambda: self.close())

        # Bouton Menu
        self.caves_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.caves_page))
        self.vins_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.vins_page))
        self.cepages_blancs_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.cepages_blancs_page))
        self.cepages_rouges_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.cepages_rouges_page))
        self.vins_cepages_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.vins_cepages_page))
        self.cuves_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.cuves_page))
        self.tournees_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.tournees_page))
        self.tchat_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.tchat_page))

        # Help
        self.pushButton_about.clicked.connect(lambda: self.toggle_body_right())

    def toggle_body_right(self):
        if self.body_right.isHidden():
            self.body_right.show()
        else:
            self.body_right.hide()


    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
            self.pushButton_maxi_windows.setIcon(QtGui.QIcon(u":/newPrefix/image/maximize-window-32.png"))
        else:
            self.showMaximized()
            self.pushButton_maxi_windows.setIcon(QtGui.QIcon(u":/newPrefix/image/maximize-window-32.png"))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = True
            # Capture de la position relative de la souris par rapport à la fenêtre
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable:
            # Calculer la nouvelle position de la fenêtre
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())





