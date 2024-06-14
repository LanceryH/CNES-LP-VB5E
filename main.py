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
    ui.show()
    
    app.exec_()
    