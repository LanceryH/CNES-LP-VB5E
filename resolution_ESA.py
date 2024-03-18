import numpy as np
from scipy.optimize import leastsq
from scipy.stats import linregress
import matplotlib.pyplot as plt

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
        self.Ke = None
        self.h = 0.0012  # thickness in meters
        self.l = 0.010 # Length of the material in meters
        self.n = 0.010 # Width of the material in meters
        self.R = 8.314  # J/(mol·K) Universal gas constant
        self.Kelvin_cte = 273.15
        self.m_initial = 14.4708/1000 #g
        self.mu_i_0 = 0 #initial mass that could be potentially be outgassed
        self.tronq = 40
        self.result_dic = {"parameter_exp" : [],
                           "coeff_transition" : [],
                           "fitted data exp" : [],
                           "fitted data exp small" : [],
                           "X_3D" : [],
                           "Y_3D" : [],
                           "Z_3D" : [],
                           "X_3D_smooth" : [],
                           "X_3D_smooth" : [],
                           "Y_3D_smooth" : [],
                           "Z_3D_smooth" : [],
                           "fitted data 5exp" : []}

    def Initialisation(self):
        for ind in range(6):
            self.data_expo["tau"][ind] = 0.5
            self.data_expo["mi"][ind] = 0.002

    def function_TML(self, *params, time):
        sum = 0
        tau_s = np.absolute(params[:6])
        m_i = np.absolute(params[6:])
        for i in range(len(tau_s)):            
            sum += m_i[i]*(1-np.exp(-np.array(time)/tau_s[i]))
        return sum

    def function_TML_simmu(self, *params, time, temp, Tref):
        sum = 0
        tau_s = params[0][:6]
        m_i = params[0][6:]
        #print(m_i)
        
        for i in range(len(tau_s)):   
            tau_T = tau_s[i]*np.exp(-self.Ke*(temp-Tref))         
            sum += m_i[i]*(1-np.exp(-time/tau_T))
        return sum
    
    def function_TML_fit(self,n=6): 
        
        # Méthode des moindres carrés
        x0 = self.data_expo["tau"]
        x0.extend(self.data_expo["mi"])

        for ind_i in range(5):
            params_lsq = np.absolute(leastsq(self.objective, x0, args=(ind_i), maxfev=2000)[0])
            exp_i = self.function_TML(*params_lsq, time=self.table_data["time_tot_reshaped"][ind_i])
            exp_o = self.function_TML(*params_lsq, time=self.table_data["time_tot_tot"])
            self.result_dic["parameter_exp"].append(params_lsq)
            self.result_dic["fitted data exp"].append(exp_o)
            self.result_dic["fitted data exp small"].append(exp_i) 
            self.result_dic["fitted data 5exp"].extend(exp_i+self.table_data["mu"][ind_i][0])
        #plt.figure()
        Ki = 1
        for ind_i in range(4):

            d_m_2 = self.result_dic["fitted data 5exp"][(ind_i+1)*24*60+500] - self.result_dic["fitted data 5exp"][(ind_i+1)*24*60]
            d_T_2 = self.table_data["time_tot_tot"][(ind_i+1)*24*60+500] - self.table_data["time_tot_tot"][(ind_i+1)*24*60]
            
            d_m_1 = self.result_dic["fitted data 5exp"][(ind_i+1)*24*60] - self.result_dic["fitted data 5exp"][(ind_i+1)*24*60-500]
            d_T_1 = self.table_data["time_tot_tot"][(ind_i+1)*24*60] - self.table_data["time_tot_tot"][(ind_i+1)*24*60-500]

            Ki_i1 = (d_m_2/d_T_2)/(d_m_1/d_T_1)
            Ea = np.log(Ki_i1)*self.R*self.table_data["time"][ind_i][2]*self.table_data["temp"][ind_i+1][2]/(self.table_data["temp"][ind_i+1][2]-self.table_data["temp"][ind_i][2])
            self.result_dic["coeff_transition"].append([Ki_i1*Ki,Ea])
            print("Ki_i1",Ki_i1)
            Ki=Ki_i1*Ki

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

        plt.figure()
        list_test= []
        for ind in range(4):
            list_test.append(self.result_dic["coeff_transition"][ind][0])
        self.Ke, intercept, r, p, se = linregress(temp[:-1], np.log(list_test))
        plt.scatter(temp[:-1], np.log(list_test))
        plt.plot(temp[:-1], intercept + self.Ke*np.array(temp[:-1]), 'r', label="fitted line")
        #plt.show()
        return 

    def objective(self, x, ind_i):
        return np.array(self.table_data["mu_tot_reshaped"][ind_i]) - np.array(self.function_TML(*x, time=self.table_data["time_tot_reshaped"][ind_i]))


