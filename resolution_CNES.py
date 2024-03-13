import numpy as np
from scipy.optimize import leastsq
from scipy.interpolate import interp1d
from tqdm import tqdm
import matplotlib.pyplot as plt
class Equations_CNES:
    def __init__(self, table_data, data_expo, nb_exp, mu_i_0=0):
        self.table_data = table_data
        self.data_expo = data_expo
        self.nb_exp = nb_exp
        self.A_i = None
        self.E_i = None
        self.k_i_t = None
        self.tau_1 = None
        self.tau_2 = None
        self.T_p_1 = None
        self.T_p_2 = None
        self.Kelvin_cte = 273.15
        self.tronq = 40
        self.mu_i_0 = 0.01 #initial mass that could be potentially be outgassed
        self.R_cte = 1.986 #cal.mol-1.K-1
        self.result_dic = {"parameter exp" : [],
                           "fitted data exp" : [],
                           "X_3D" : [],
                           "Y_3D" : [],
                           "Z_3D" : [],
                           "X_3D_smooth" : [],
                           "X_3D_smooth" : [],
                           "Y_3D_smooth" : [],
                           "Z_3D_smooth" : [],
                           "fitted data 5exp" : 0}
        
    def Initialisation(self):
        for ind in range(len(self.table_data["mu"])):
            self.data_expo["E"][ind] = 1500 * ind + 500
            self.data_expo["A"][ind] = ind*10**ind + 0.001
            self.data_expo["mu"][ind] = 0.8


    def function_TML(self, *params):
        n = len(params)//3
        nb_points = len(self.table_data["temp_tot"])
        sum = np.zeros(5)
        mu_t = np.zeros(nb_points)
        A_s = params[:n]
        E_s = params[n:n*2]
        mi_s = params[n*2:]
        for i in range(1,nb_points):
            temp_moy = self.table_data["temp_tot"][i-1] + (self.table_data["temp_tot"][i] - self.table_data["temp_tot"][i-1])/2
            for j in range (n):
                Dt = self.table_data["time_tot"][i] - self.table_data["time_tot"][i-1]
                k_i = A_s[j]*np.exp(-E_s[j]/(self.R_cte*temp_moy))
                We = (mi_s[j]-sum[j])*(1-np.exp(-1*Dt*k_i))
                sum[j] += We
                mu_t[i] = sum[j]
            
        return mu_t
    
    def function_TML_full(self, *params, temp=25):
        n = len(params)//3
        nb_points = len(self.table_data["temp_tot"])
        sum = np.zeros(5)
        mu_t = np.zeros(nb_points)
        A_s = params[:n]
        E_s = params[n:n*2]
        mi_s = params[n*2:]
        for i in range(1,nb_points):
            for j in range (n):
                Dt = (24*60//self.tronq)
                k_i = A_s[j]*np.exp(-E_s[j]/(self.R_cte*temp))
                We = (mi_s[j]-sum[j])*(1-np.exp(-1*Dt*k_i))
                sum[j] += We
                mu_t[i] = sum[j]
        return mu_t
        
    def function_TML_fit(self):
                
        # Méthode des moindres carrés
        for ind_i in range(self.nb_exp):
            param_i = [self.data_expo["A"][ind_i],self.data_expo["E"][ind_i],self.data_expo["mu"][ind_i]]
            params_lsq = leastsq(self.objective, param_i, args=(ind_i), maxfev=4000)[0]
            exp_i = self.function_TML(*params_lsq, ind_i)
            self.result_dic["parameter exp"].append(params_lsq)
            self.result_dic["fitted data exp"].append(exp_i) 
            self.result_dic["fitted data 5exp"] += exp_i

        # Enregistrement des data
        temp = [25,50,75,100,125]
        precision_3D = 100
        sum_of_exp = []
        for ind_i in range(5):
            integral_of_arr = 0
            self.result_dic["X_3D"] = self.table_data["time_tot"]
            self.result_dic["Y_3D"].append(np.ones(len(self.table_data["time_tot"]))*temp[ind_i])
            for ind_j in range(ind_i+1):
                integral_of_arr += self.function_TML_full(*self.result_dic["parameter exp"][ind_j],temp=temp[ind_j]) 
            sum_of_exp.append(integral_of_arr)    
        self.result_dic["Z_3D"] = np.array(sum_of_exp)

        # Régression polynomiale ordre 4
        Z_liss = []
        for ind_i in range(5*24*60//self.tronq):
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
        if ind == 0:
            return np.array(self.table_data["mu_tot"])[:24*60*1//self.tronq] - np.array(self.function_TML(*x))[:24*60*1//self.tronq]
        elif ind == 1:
            return np.array(self.table_data["mu_tot"]-self.function_TML(*self.result_dic["parameter exp"][0]))[:24*60*2//self.tronq] - np.array(self.function_TML(*x))[:24*60*2//self.tronq]
        elif ind == 2:
            return np.array(self.table_data["mu_tot"]-self.function_TML(*self.result_dic["parameter exp"][1])-self.function_TML(*self.result_dic["parameter exp"][0]))[:24*60*3//self.tronq] - np.array(self.function_TML(*x))[:24*60*3//self.tronq]
        elif ind == 3:
            return np.array(self.table_data["mu_tot"]-self.function_TML(*self.result_dic["parameter exp"][2])-self.function_TML(*self.result_dic["parameter exp"][1])-self.function_TML(*self.result_dic["parameter exp"][0]))[:24*60*4//self.tronq] - np.array(self.function_TML(*x))[:24*60*4//self.tronq]
        elif ind == 4:
            return np.array(self.table_data["mu_tot"]-self.function_TML(*self.result_dic["parameter exp"][3])-self.function_TML(*self.result_dic["parameter exp"][2])-self.function_TML(*self.result_dic["parameter exp"][1])-self.function_TML(*self.result_dic["parameter exp"][0]))[:24*60*5//self.tronq] - np.array(self.function_TML(*x))[:24*60*5//self.tronq]
    