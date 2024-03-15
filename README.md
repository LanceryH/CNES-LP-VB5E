-----
## Prédiction du dégazage méthode MC CNES
----
### Définition du sujet

nombre d'exponentielles $n=5$

### $$k^{(t)}_i = A_i e^{\frac{E_i}{RT^{(t)}}}$$
### $$\mu^{(t)}=\sum_{i=1}^{n} \int_{t_0}^{t}\mu_i (1-e^{-dt. k^{(t)}_i})$$

L'algorithme consiste à minimiser l'erreur de la fonction (moindre carré) en ajustant les paramètres suivant la minimisation 

Chaque palier de température de la cinétique se voit attribué une espèce chimique approximé par une exponentielle

----
### Application python

Fonction solution de l'équation de masse pour chaque espèce chimique 
[code Ref.1](https://github.com/LanceryH/Cnes_LP_VB5E/blob/b09f277af6533a65b18a40ce6191ed4f0d6e2bc0/resolution_CNES_M.py#L38C5-L49C19)

```python
def function_TML(self, *params, time=0, temp=25):
      sum = 0
      A_s = params[:n]
      E_s = params[n:n*2]
      Mi_s = params[n*2:]
      k_i_t = A_s[j]*np.exp(-E_s[j]/(self.R_cte*temp))
      sum += (mi_s[0])*(1-np.exp(-np.array(time)*k_i_t))
      return sum
```
Fonction applicant les moindres carrées sur l'équation 
[code Ref.2](https://github.com/LanceryH/Cnes_LP_VB5E/blob/cab1dc12d166c8ba1ab3f4c076725c6f098306b8/resolution_CNES_M.py#L51C1-L63C102)

```python
def function_TML_fit(self):
        exp_list = []
        for ind_i in range(self.nb_exp):
            x = [self.data_expo["A"][ind_i],
                 self.data_expo["E"][ind_i],
                 self.data_expo["mu"][ind_i]]
            self.params_lsq = leastsq(self.objective, x, args=(ind_i), maxfev=5000)[0]
            exp_i = self.function_TML(*self.params_lsq,
                                       time=self.table_data["time_tot_tot"],
                                       temp=self.table_data["temp"][ind_i][1])
            exp_list.append(exp_i)
    return exp_list
```
Fonction de minimisation
[code Ref.3](https://github.com/LanceryH/Cnes_LP_VB5E/blob/93cd4022814937dadaf33ea915ee3a8b973c9860/resolution_CNES_M.py#L93C4-L94C189)

```python
def objective(self, x, ind):
      init_0_mu = np.array(self.table_data["mu"][ind]) - self.table_data["mu"][ind][0]
      mu_calc = np.array(self.function_TML(*x,
                                            time=self.table_data["time"][0],
                                            temp=self.table_data["temp"][ind][1]))
      return init_0_mu - mu_calc
```
-----
### Initialisation de chaque exponentielle

L'algorithme est trés sensible aux paramètres initiaux (gradient qui ne converge pas)

| Input parameters  | Value / $i \in (1,2,3,4,5)$|
| :---: | :---: |
| $E_i$ | $1500i + 500$  |
| $A_i$ | $i10^i + 0.001$  |
| $\mu_i$ | 0.8  |

Initialisation des paramètres [code Ref.4](https://github.com/LanceryH/Cnes_LP_VB5E/blob/cab1dc12d166c8ba1ab3f4c076725c6f098306b8/resolution_CNES_M.py#L32C5-L36C44)

-----
<img src="https://github.com/LanceryH/Cnes_LP_VB5E/assets/108919405/c809cb9b-ffea-4719-90ca-2823a25a7d4f" alt="drawing" width="50%" height="50%"/>

-----
## Prédiction du dégazage méthode MC ESA 
----
### Définition du sujet

Il s'agit de la même méthode mais pour chaque palier/exponentielle, 6 espèces chimiques sont considérées

### $$k^{(t)}_i = A_i e^{\frac{E_i}{RT^{(t)}}}$$
### $$j \in (1,2,3,4,5)$$
### $$n \in  ⟦ 4,9 ⟧$$
### $$\mu_j=\sum_{i=1}^{n}\mu_i (1-e^{-\frac{dt}{\tau_i}})$$

L'algorithme conciste à miniser l'erreur de la fonction (moindres carrées) en ajustant les paramètres suivant la méthode des gradients

Chaque palier de température de la cinétique se voit attribué une espèce chimique approximé par une exponentielle

----
<img src="https://github.com/LanceryH/Cnes_LP_VB5E/assets/108919405/22659e6b-770d-4d23-ae27-855e5e59ab9d" alt="drawing" width="50%" height="50%"/>

## Régression polynomiale du maillage
<img src="https://github.com/LanceryH/Cnes_LP_VB5E/assets/108919405/f837df3a-7439-4373-a00c-1876256ed137" alt="drawing" width="50%" height="50%"/>

