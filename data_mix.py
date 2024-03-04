# Initialisation des données
import os
import pandas as pd
import numpy as np

def clear_data(dir_path, nb_exp = 5):
    df = pd.read_excel(dir_path, sheet_name="Feuil1")
    temp_values = np.ones(5*24*60)
    table_expo = {}
    for ind in range(1,nb_exp+1):
            temp_values[(ind-1)*24*60:ind*24*60] = 25*ind

    time_sep = []
    mu_sep = []
    temp_sep = []
    time_tot = []
    mu_tot = []
    temp_tot = []
    for ind in range (nb_exp):
        df["Temperature"] = pd.DataFrame(temp_values)
        time_sep.append(df['Time [minutes]'][ind*60*24:(ind+1)*60*24].to_list())
        mu_sep.append(df['TML (%)'][ind*60*24:(ind+1)*60*24].to_list())
        temp_sep.append(df["Temperature"][ind*60*24:(ind+1)*60*24].to_list())
        time_tot.extend(df['Time [minutes]'][ind*60*24:(ind+1)*60*24].to_list())
        mu_tot.extend(df['TML (%)'][ind*60*24:(ind+1)*60*24].to_list())
        temp_tot.extend(df["Temperature"][ind*60*24:(ind+1)*60*24].to_list())
    
    
    table_expo["time"] = time_sep
    table_expo["mu"] = mu_sep
    table_expo["temp"] = temp_sep
    table_expo["time_tot"] = time_tot
    table_expo["mu_tot"] = mu_tot
    table_expo["temp_tot"] = temp_tot
    
    data_expo = {"mu":[1,1,1,1,1],
                 "E":[1,1,1,1,1],
                 "A":[1,1,1,1,1],
                 "Alpha":[1,1,1,1,1],
                 "Ka":0}
    
    M_rearranged = []
    for ind in range(5):
        M_rearranged.extend(np.array(table_expo["mu"][ind])-np.array(table_expo["mu"][ind])[0])
    table_expo["mu_tot_reshaped"] = M_rearranged

        
    M_rearranged = np.ones(5*24*60)
    M_rearranged[:24*60] = table_expo["mu_tot"][:24*60]
    M_rearranged[24*60:] = M_rearranged[24*60:]*table_expo["mu"][0][-1]
    table_expo["mu_tot_separated"] = [np.array(M_rearranged)]

    M_rearranged = np.ones(5*24*60)
    M_rearranged[:2*24*60] = table_expo["mu_tot"][:2*24*60]
    M_rearranged[2*24*60:] = M_rearranged[2*24*60:]*table_expo["mu"][1][-1]
    table_expo["mu_tot_separated"].append(list(M_rearranged))

    M_rearranged = np.ones(5*24*60)
    M_rearranged[:3*24*60] = table_expo["mu_tot"][:3*24*60]
    M_rearranged[3*24*60:] = M_rearranged[3*24*60:]*table_expo["mu"][2][-1]
    table_expo["mu_tot_separated"].append(list(M_rearranged))

    M_rearranged = np.ones(5*24*60)
    M_rearranged[:3*24*60] = table_expo["mu_tot"][:3*24*60]
    M_rearranged[3*24*60:] = M_rearranged[3*24*60:]*table_expo["mu"][3][-1]
    table_expo["mu_tot_separated"].append(list(M_rearranged))


    return table_expo, data_expo