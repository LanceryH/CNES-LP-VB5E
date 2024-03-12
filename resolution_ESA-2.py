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
        self.result_dic = {"parameter exp" : [],
                           "fitted data exp" : [],
                           "X_3D" : [],
                           "Y_3D" : [],
                           "Z_3D" : [],
                           "X_3D_smooth" : [],
                           "X_3D_smooth" : [],
                           "Y_3D_smooth" : [],
                           "Z_3D_smooth" : [],
                           "fitted data 5exp" : []}

    def Initialisation(self):
        for ind in range(len(self.table_data["mu"])):
            self.data_expo["E"][ind] = 1500 * ind + 1000
            self.data_expo["Alpha"][ind] = 0.9
        self.data_expo["Alpha"][-1] =  1.5

    def function_TML(self, *params, time):
        sum = 0
        tau_s = params[:-1]
        m_i = params[-1]
        for i in range(len(tau_s)):            
            sum += m_i*(1-np.exp(-np.array(time)/tau_s[i]))
            m_i -= m_i*sum[-1]
        return sum

    def function_TML_fit(self,n=6): 
        
        # Méthode des moindres carrés
        last_value = 0
        for ind_i in range(5):
            x0=np.ones(n+1)
            x0[-1]=self.m_initial
            params_lsq = leastsq(self.objective, x0, args=(ind_i), maxfev=2000)[0]
            exp_i = self.function_TML(*params_lsq, time=self.table_data["time_tot_reshaped"][ind_i])
            self.result_dic["parameter exp"].append(params_lsq)
            self.result_dic["fitted data exp"].append(exp_i) 
            self.result_dic["fitted data 5exp"].extend(exp_i+last_value)
            last_value += exp_i[-1]

        d_m_T2 = (exp_i[-1] - exp_i[-2])/(self.table_data["time"][1][-1] - self.table_data["time"][1][0])
        d_m_T1 = (exp_i[1] - exp_i[0])/(self.table_data["time"][0][-1] - self.table_data["time"][0][0])
        ka = d_m_T2/d_m_T1
        print(self.table_data["temp"][1][0],self.table_data["temp"][0][0])
        Ea = np.log(ka)*self.R*self.table_data["temp"][0][0]*self.table_data["temp"][1][0]/(self.table_data["temp"][1][0]-self.table_data["temp"][0][0])
        print(ka,Ea)
        return 

    def objective(self, x, ind_i):
        return np.array(self.table_data["mu_tot_reshaped"][ind_i]) - np.array(self.function_TML(*x, time=self.table_data["time_tot_reshaped"][ind_i]))


