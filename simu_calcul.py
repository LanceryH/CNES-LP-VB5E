from app import *
import os
from PyQt5.QtWidgets import QApplication
import sys
from resolution_CNES_M import *
import warnings
warnings.filterwarnings('ignore')
dir_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    table_data, data_expo = clear_data(dir_path+"/Données/EC9323-2.xls")
    #table_data, data_expo = clear_data("C:/Users/Lance/Documents/Codes_win/Python/CNES LP_VB5E/Données/EC2216.xls")
    system = Equations_CNES_M(table_data, data_expo)
    system.Initialisation()
    system.function_TML_fit()

