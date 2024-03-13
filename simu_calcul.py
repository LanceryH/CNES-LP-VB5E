from app import *
import os
from PyQt5.QtWidgets import QApplication
import sys
from resolution_ESA import *
import warnings
warnings.filterwarnings('ignore')
dir_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    table_data, data_expo = clear_data("C:/Users/Lance/Documents/Codes_win/Python/CNES LP_VB5E/Données/EC9323-2.xls")
    #table_data, data_expo = clear_data("C:/Users/Lance/Documents/Codes_win/Python/CNES LP_VB5E/Données/EC2216.xls")
    system = Equations_ESA(table_data, data_expo)
    system.Initialisation()
    system.function_TML_fit(n=6)

   
    plt.figure()
    plt.plot(table_data["time_tot_tot"],table_data["mu_tot_tot"],"b", label="data")
    plt.plot(table_data["time_tot_tot"],system.result_dic["fitted data 5exp"],"r--", label="data")
    #self.axs_2D[0].plot(table_data["time_tot_tot"],system.result_dic["fitted data 5exp"],"r--", label="prediction n=5 cnes")
    for ind_i in range(len(system.result_dic["fitted data exp"])):
        plt.plot(table_data["time"][ind_i],table_data["mu_tot_reshaped"][ind_i],"b", label="data")
        plt.plot((np.array(table_data["time_tot_tot"])+(24*60*ind_i))[:24*60*(5-ind_i)],
                        system.result_dic["fitted data exp"][ind_i][:24*60*(5-ind_i)],
                        "r--",
                        label=f"Expo {ind_i+1}",
                        linewidth=1)
    plt.grid()
    plt.show()
