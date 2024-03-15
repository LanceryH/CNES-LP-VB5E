import numpy as np
from scipy.optimize import leastsq
from tqdm import tqdm
import matplotlib.pyplot as plt
class Equations_CNES_M:
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
        self.nb_exp = 5
        self.Kelvin_cte = 273.15
        self.mu_i_0 = 0.01 #initial mass that could be potentially be outgassed
        self.R_cte = 1.986 #cal.mol-1.K-1
        self.tronq = 40
        self.result_dic = {"parameter_exp" : [],
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
            self.data_expo["E"][ind] = 1500 * ind + 500
            self.data_expo["A"][ind] = ind*10**ind + 0.001
            self.data_expo["mu"][ind] = 0.8

    def function_TML(self, *params, time=0, temp=25):
        n = len(params)//3
        sum = 0
        A_s = params[:n]
        E_s = params[n:n*2]
        mi_s = params[n*2:]

        for j in range(1):
            k_i_t = A_s[j]*np.exp(-E_s[j]/(self.R_cte*temp))
            sum += (mi_s[j])*(1-np.exp(-np.array(time)*k_i_t))
        return sum

    def function_TML_simmu(self, *params, time, temp):
        A_s = params[0][0]
        E_s = params[0][1]
        mi_s = params[0][2]
        k_i = A_s*np.exp(-E_s/(self.R_cte*temp))
        mu_t = mi_s*(1-np.exp(-1*time*k_i))
        return mu_t
    
    def function_TML_fit(self):
        "As,Es,ms"

        # Méthode des moindres carrés
        for ind_i in range(self.nb_exp):
            x = [self.data_expo["A"][ind_i],
                self.data_expo["E"][ind_i],
                self.data_expo["mu"][ind_i]]
            self.params_lsq = leastsq(self.objective, x, args=(ind_i), maxfev=5000)[0]
            exp_i = self.function_TML(*self.params_lsq, time=self.table_data["time_tot_tot"], temp=self.table_data["temp"][ind_i][1])
            self.result_dic["parameter_exp"].append(self.params_lsq)
            self.result_dic["fitted data exp"].append(exp_i) 
            self.result_dic["fitted data 5exp"].extend(exp_i[:24*60]+self.table_data["mu"][ind_i][0])
            
        # Enregistrement des data
        temp = [25,50,75,100,125]
        precision_3D = 100
        sum_of_exp = []
        for ind_i in range(5):
            integral_of_arr = np.zeros(len(self.result_dic["fitted data exp"][0]))
            self.result_dic["X_3D"] = self.table_data["time_tot"]
            self.result_dic["Y_3D"].append(np.ones(len(self.table_data["time_tot"]))*temp[ind_i])
            for ind_j in range(ind_i+1):
                integral_of_arr += np.array(self.result_dic["fitted data exp"][ind_j])
            sum_of_exp.append(integral_of_arr)    
        self.result_dic["Z_3D"] = np.array(sum_of_exp)

        # Régression polynomiale ordre 4
        Z_liss = []
        for ind_i in range(0,5*24*60,self.tronq):
            coeffs = np.polyfit(temp, self.result_dic["Z_3D"][:,ind_i], 4)
            polynomial = np.poly1d(coeffs)
            t = np.linspace(min(temp),max(temp),precision_3D)
            new_v = polynomial(t)
            Z_liss.append(new_v)
        self.result_dic["Z_3D_smooth"] = np.array(Z_liss).T
        xx = self.table_data["time_tot"]
        yy = np.linspace(min(temp),max(temp),precision_3D)
        self.result_dic["X_3D_smooth"], self.result_dic["Y_3D_smooth"] = np.meshgrid(xx, yy)
        return 


    def objective(self, x, ind):
        return np.array(self.table_data["mu"][ind]) - self.table_data["mu"][ind][0] - np.array(self.function_TML(*x, time=self.table_data["time"][0], temp=self.table_data["temp"][ind][1]))


