import numpy as np
from scipy.optimize import leastsq
from tqdm import tqdm
import matplotlib.pyplot as plt
class Equations_CNES:
    def __init__(self, table_data, data_expo, mu_i_0=0):
        self.table_data = table_data
        self.data_expo = data_expo
        self.A_i = None
        self.E_i = None
        self.k_i_t = None
        self.tau_1 = None
        self.tau_2 = None
        self.T_p_1 = None
        self.T_p_2 = None
        self.Kelvin_cte = 273.15
        self.mu_i_0 = 0.01 #initial mass that could be potentially be outgassed
        self.R_cte = 1.986 #cal.mol-1.K-1

    def Initialisation(self):
        for ind in range(len(self.table_data["mu"])):
            self.data_expo["E"][ind] = 1500 * ind + 1000
            self.data_expo["Alpha"][ind] = 0.9
        self.data_expo["Alpha"][-1] =  1.5

    def function_TML(self, *params):
        n = len(params)//3
        sum = np.zeros(24*60*5)
        A_s = params[:n]
        E_s = params[n:n*2]
        mi_s = params[n*2:]
        print(f"E_s :{E_s}")
        print(f"A_s :{A_s}")
        print(f"mi_s :{mi_s}")

        for i in range(0,n):
            for j in range (i+1):
                k_i_t = A_s[j]*np.exp(-E_s[j]/(self.R_cte*self.table_data["temp"][j][1]))
                sum[i*24*60:(i+1)*24*60] += (mi_s[i])*(1-np.exp(-np.array(self.table_data["time"][j])*k_i_t))#-sum[(i+1)*24*60-1]
        return sum

    def function_TML_fit(self):
        "As,Es,ms"
        x0 = [1,1,1,1,1,1000,2250,1500,1750,2500,0.5,0.5,0.5,0.5,0.5]

        params_lsq = leastsq(self.objective, x0, maxfev=5000)[0]
        data = []

        for ind in range(len(x0)//3):
            data.extend([0,params_lsq[ind*2],params_lsq[ind*2+1]])
        
        data = self.function_TML(*params_lsq)
        data_reshaped = np.zeros(5*24*60)
        data_reshaped[:24*60] = data[:24*60]
        for ind in range(1,5):
            data_reshaped[ind*24*60:(ind+1)*24*60] = data[ind*24*60:(ind+1)*24*60]+data_reshaped[(ind)*24*60-1]

        plt.figure()
        plt.plot(self.table_data["time_tot"],self.table_data["mu_tot_reshaped"],label="data")
        plt.plot(self.table_data["time_tot"],data,label="fit")
        plt.plot(self.table_data["time_tot"],self.table_data["mu_tot"],label="data")
        plt.plot(self.table_data["time_tot"],data_reshaped,label="fit")
        plt.show()

        return data_reshaped, data

    def objective(self, x):
        return np.array(self.table_data["mu_tot_reshaped"]) - np.array(self.function_TML(*x))
