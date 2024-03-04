import numpy as np
from scipy.optimize import leastsq
from tqdm import tqdm
import matplotlib.pyplot as plt
class Equations_CNES_2:
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

        for i in range(0,n):
            for j in range(i+1):
                k_i_t = A_s[j]*np.exp(-E_s[j]/(self.R_cte*self.table_data["temp"][j][1]))
                sum += (mi_s[i])*(1-np.exp(-np.array(self.table_data["time_tot"])*k_i_t))#-sum[(i+1)*24*60-1]
        return sum

    def function_TML_fit(self):
        "As,Es,ms"
        
        x0 = [0.7,
              1000,
              0.5]
        self.params_lsq0 = leastsq(self.objective, x0, maxfev=5000)[0]

        x1 = [0.7,
              0.7,
              500,
              1500,
              0.5,
              0.5]
        self.params_lsq1 = leastsq(self.objective1, x1, maxfev=5000)[0]

        x2 = [0.7,
              0.7,
              0.7,
              500,
              1500,
              3000,
              0.5,
              0.5,
              0.5]
        self.params_lsq2 = leastsq(self.objective2, x2, maxfev=5000)[0]

        data = self.function_TML(*self.params_lsq0)

        plt.figure()
        plt.plot(self.table_data["time_tot"],data)
        plt.plot(self.table_data["time_tot"],self.table_data["mu_tot"])
        plt.show()

        return data, data

    def objective(self, x):
        return np.array(self.table_data["mu_tot"][:24*60]) - np.array(self.function_TML(*x)[:24*60])
    def objective1(self, x):#
        return np.array(self.table_data["mu_tot"][:2*24*60]) - np.array(self.function_TML(*x)[:2*24*60])
    def objective2(self, x):
        return np.array(self.table_data["mu_tot"]) - np.array(self.function_TML(*self.params_lsq1)) - np.array(self.function_TML(*x))
