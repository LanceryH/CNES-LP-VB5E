from app import *
import os
from PyQt5.QtWidgets import QApplication
import sys
from resolution_CNES import *
dir_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    table_data, data_expo = clear_data(dir_path+"\Données\EC9323-2.xls")

    system_CNES = Equations_CNES(table_data, data_expo)
    system_CNES.Initialisation()

    mu_t_CNES, params = system_CNES.function_TML_fit()
