import numpy as np
from scipy.optimize import leastsq

class Equations_ESA:
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
        self.h = 0.0012  # thickness in meters
        self.l = 0.010 # Length of the material in meters
        self.n = 0.010 # Width of the material in meters
        self.R = 8.314  # J/(mol·K) Universal gas constant
        self.Kelvin_cte = 273.15
        self.m_initial = 14.4708/1000 #g
        self.mu_i_0 = 0 #initial mass that could be potentially be outgassed

    def Initialisation(self):
        for ind in range(len(self.table_data["mu"])):
            self.data_expo["E"][ind] = 1500 * ind + 1000
            self.data_expo["Alpha"][ind] = 0.9
        self.data_expo["Alpha"][-1] =  1.5

    def function_TML(self, *params):
        sum = 0
        tau_s = params[:-1]
        m_i = params[-1]
        for i in range(len(tau_s)):            
            sum += m_i*(1-np.exp(-np.array(self.table_data["time"][0])/tau_s[i]))
            m_i -= m_i*sum[-1]
        return sum

    def function_TML_fit(self,n=6):
        x0=np.ones(n+1)
        x0[-1]=self.m_initial
        params_lsq = leastsq(self.objective, x0, maxfev=2000)[0]
        #print(params_lsq)
        return self.function_TML(*params_lsq)

    def objective(self, x):
        return self.table_data["mu"][0] - self.function_TML(*x)

