import numpy as np
from scipy.optimize import leastsq
from tqdm import tqdm

class Equations_ONERA:
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
        self.mu_i_0 = 0.01 #initial mass that could be potentially be outgassed
        self.R_cte = 1.986 #cal.mol-1.K-1
        self.r_t0 = 0
        self.r_t1 = 5
        self.r_t2 = 18
        self.sqrt_t = np.sqrt(self.table_data["time"][0])
        self.tau = None
        
    def Initialisation(self):
        for ind in range(len(self.table_data["mu"])):
            self.data_expo["E"][ind] = 1500 * ind + 1000
            self.data_expo["Alpha"][ind] = 0.9
        self.data_expo["Alpha"][-1] =  1.5

    def function_TML(self, *params):
        D = params[0]
        M0 = params[1]
        self.tau = 1000
        t = np.array(self.table_data["time"][0])
        M_fit = np.zeros(len(t))
        # Calculate fit using the appropriate equation based on time range
        M_fit[t < self.tau] = D *  M0 / self.h  * np.sqrt(np.pi*self.tau) * np.sqrt(t[t < self.tau])
        M_fit[t >= self.tau] = 8 * M0 * self.h / (np.pi) * (1 - np.exp(-(t[t >= self.tau] - t[t < self.tau][-1]) / self.tau)) + M_fit[t < self.tau][-1]
        return M_fit

    def function_TML_fit(self):
        # Calculate the index of the square root of t0, t1 and t2 values
        self.t_0_index = np.argmin(np.abs(self.sqrt_t - self.r_t0))
        self.t_1_index = np.argmin(np.abs(self.sqrt_t - self.r_t1))
        self.t_2_index = np.argmin(np.abs(self.sqrt_t - self.r_t2))
        self.t_m_index = len(self.table_data["time"][0])
        
        # Calculate slope and coefficient D
        self.slope, self.b = np.polyfit(self.sqrt_t[self.t_1_index:self.t_2_index], self.table_data["mu"][0][self.t_1_index:self.t_2_index], 1)
        Mm = np.max(self.table_data["mu"][0])
        
        # Calcul of inital values for the curve fitting
        #D = np.pi*((self.h/(4*Mm))**2)*self.slope**2
        #Dx = D*(1+self.h/self.l+self.h/self.n)**-2 #edge effects
        #tau = self.h**2/D
        x0 = [5e-10, 13]
        params_lsq = leastsq(self.objective, x0, maxfev=2000)[0]
        return self.function_TML(*params_lsq)
    
    def objective(self, x):
        return np.array(self.table_data["mu"][0]) - np.array(self.function_TML(*x))
