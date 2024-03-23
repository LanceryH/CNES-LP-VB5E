from app import *
import os
from PyQt5.QtWidgets import QApplication
import sys
import warnings
if getattr(sys, 'frozen', False):
    import pyi_splash

if __name__ == '__main__':

    warnings.filterwarnings('ignore')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    app = QApplication(sys.argv)
    ui = Ui()
    if getattr(sys, 'frozen', False):
        pyi_splash.close()
    msg = QMessageBox()
    msg.setWindowTitle("Aide")
    msg.setText("Merci de séléctionner un fichier \n -> menu 'Fichier' \n -> cliquer 'Ouvrir'")
    msg.setIcon(QMessageBox.Information)
    msg.exec_()
    ui.show()
    
    app.exec_()
    