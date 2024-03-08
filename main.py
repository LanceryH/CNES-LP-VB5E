from app import *
import os
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    app = QApplication(sys.argv)
    ui = Ui()
    ui.show()
    app.exec_()
    