
# Prédiction et modélisation du dégazage LPVB5E

### Méthode CNES

Considération de 5 espèces chimiques dégazées avec une volatilité décroissante.

### $$\forall i \in ⟦ 1,n ⟧, \quad E_i>E_{i-1}$$
### $$k^{(t)}_i = A_i e^{\frac{E_i}{RT^{(t)}}}$$
### $$n = 5$$
### $$\mu^{(t)}=\sum_{i=1}^{n} \int_{t_0}^{t}(\mu_i-\mu^{(t)}_i) (1-e^{-dt. k^{(t)}_i})$$

### Méthode ESA

Considération de 6 espèces chimiques dégazées par pallier.

### $$k^{(t)}_i = A_i e^{\frac{E_i}{RT^{(t)}}}$$
### $$\tau_i = \frac{1}{k^{(t)}_i}$$
### $$j \in ⟦ 1,5 ⟧$$
### $$n \in  ⟦ 4,9 ⟧$$
### $$\mu_j=\sum_{i=1}^{n}\mu_i (1-e^{-\frac{t}{\tau_i}})$$

### Fonctionnement du fitting

L'algorithme consiste à minimiser l'erreur (moindre carré) de la fonction exponentielle en ajustant les paramètres.

Chaque palier de température de la cinétique se voit attribué un certain nombre d'espèces chimiques approximé par une exponentielle.

### Paramètres d'initialisation

L'algorithme est très sensible aux paramètres initiaux (gradient qui ne converge pas).

| Paramètres initiaux CNES | $i \in ⟦ 1,n ⟧$|
| :---: | :---: |
| $E_i$ | $1500i + 500$  |
| $A_i$ | $i10^i + 0.001$  |
| $\mu_i$ | $0.8$  |

| Paramètres initiaux ESA | $i \in ⟦ 1,5 ⟧,\quad j \in ⟦ 1,n ⟧ $|
| :---: | :---: |
| $\tau^j_i$ | $[0.5,...,0.5,0.5]$ |
| $\mu^j_i$ | $[0.002,...,0.002,0.002]$  |

Initialisation des paramètres [code Ref.](https://github.com/LanceryH/Cnes_LP_VB5E/blob/cab1dc12d166c8ba1ab3f4c076725c6f098306b8/resolution_CNES_M.py#L32C5-L36C44), [code Ref.](https://github.com/LanceryH/Cnes_LP_VB5E/blob/f3e286e73476426176acfa4ac20660d5a93cb20b/resolution_ESA.py#L39C1-L42C46)

### Paramètres de sortie

| Paramètres finaux CNES |
| :---: |
| $E_i$ |
| $A_i$ |
| $\mu_i$ |

| Paramètres finaux ESA |
| :---: |
| $\tau^j_i$ |
| $\mu^j_i$ |
| $E^{i\rightarrow i+1}$ |
| $K^{i\rightarrow i+1}_e$* |

*Ke est le coéfficient directeur du facteur d'accélération vs $\Delta Température$.

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
Fonction de fitting avec les moindres carrées
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
### Résultats comparaison EC9323-2

<img src="https://github.com/LanceryH/Cnes_LP_VB5E/assets/108919405/c809cb9b-ffea-4719-90ca-2823a25a7d4f" alt="drawing" width="45%" height="45%"/>
<img src="https://github.com/LanceryH/Cnes_LP_VB5E/assets/108919405/22659e6b-770d-4d23-ae27-855e5e59ab9d" alt="drawing" width="45%" height="45%"/>
<img src="https://github.com/LanceryH/Cnes_LP_VB5E/assets/108919405/f837df3a-7439-4373-a00c-1876256ed137" alt="drawing" width="45%" height="45%"/>
<img src="https://github.com/LanceryH/Cnes_LP_VB5E/assets/108919405/ef534afa-e6d7-4db0-9614-0320905f9fe0" alt="drawing" width="45%" height="45%"/>


----
### Simulation

La simulation d'un scénario se base sur les paramètres finaux calculés au préalable pour un matériaux donné et en déduit son aspect.
Pour la méthode classique Cnes il s'agit d'une simple somme des 5 expo avec le même $T$, $t$.
### $$f(t,T) =\sum_{i=1}^{n} \int_{t_0}^{t} \mu_i (1-e^{-dt. k^{(t,T)}_i})$$

Pour la méthode du Cnes fast ou ESTEC on utilisera la fonction:

$f(t,T)$ la fonction du segment parcourue par l'algorithme.

### $$f_{a}^{b}(t,T)=\sum_{l=1}^{a} (\sum_{k=1}^{b} (\sum_{j=1}^{t^k_{max}} (\sum_{i=1}^{n_{esp}} (\mu_i (1-e^{(-\frac{t_j}{\tau_i.e^{(-K_e(T_j-T_{Ref}))}})})))+f_{l}^{k-1}(t_{max},T_{max}))+f_{l-1}^{k}(t_{max},T_{max}))$$

<img src="https://github.com/LanceryH/Cnes_LP_VB5E/assets/108919405/2015c8ba-332e-43cc-8661-9621cda7de3b" alt="drawing" width="45%" height="45%"/>
<img src="https://github.com/LanceryH/Cnes_LP_VB5E/assets/108919405/02fc81d4-582e-4aa6-bfb6-0cbe51ea6e3e" alt="drawing" width="45%" height="45%"/>

----
### Prérequis

```
pip install xlrd
pip install pandas
pip install numpy
pip install scipy
pip install PyQt5
pip install matplotlib
```
