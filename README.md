## Prédiction du dégazage méthode MC CNES

### $$k^{(t)}_i = A_i e^{\frac{E_i}{RT^{(t)}}}$$

### $$\mu_{(t)}=\sum_{i=1}^{n} \mu_i (1-e^{-dt. k^{(t)}_i}))$$

L'algorithme conciste à miniser l'erreur de la fonction (moindres carrées) en ajustant les paramètres suivant la méthode des gradients

Chaque palier de température de la cinétique se voit attribué une espèce chimique approximé par une exponentielle

| Input parameters  | Value $\forall i \in (1,2,3,4,5)$|
| :---: | :---: |
| $E_i$ | $1500i + 500$  |
| $A_i$ | $i10^i + 0.001$  |
| $\mu_i$ | 0.8  |

Algorithme implémenté: [code Ref.1](https://github.com/LanceryH/Cnes_LP_VB5E/blob/b09f277af6533a65b18a40ce6191ed4f0d6e2bc0/resolution_CNES_M.py#L38C5-L49C19)

<img src="https://github.com/LanceryH/Cnes_LP_VB5E/assets/108919405/c809cb9b-ffea-4719-90ca-2823a25a7d4f" alt="drawing" width="50%" height="50%"/>


## Prédiction du dégazage méthode MC ESA 
<img src="https://github.com/LanceryH/Cnes_LP_VB5E/assets/108919405/22659e6b-770d-4d23-ae27-855e5e59ab9d" alt="drawing" width="50%" height="50%"/>

## Régression polynomiale du maillage
<img src="https://github.com/LanceryH/Cnes_LP_VB5E/assets/108919405/f837df3a-7439-4373-a00c-1876256ed137" alt="drawing" width="50%" height="50%"/>

