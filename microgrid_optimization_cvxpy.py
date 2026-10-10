import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt

#DONNEES SYNTHETIQUES - Profil 24h
T = 24
np.random.seed(0)
P_pv = np.maximum(0, 5 * np.sin(np.linspace(0, np.pi, T)) + np.random.normal(0,0.2,T)) # kW
P_load = 2 + 1.5*np.sin(np.linspace(0, 2*np.pi, T) + 1) + np.random.normal(0,0.2,T) # kW
price_grid = np.array([0.1]*7 + [0.3]*10 + [0.1]*7) # $/kWh cher le jour

#PARAMETRES BATTERIE
E_bat_max = 10 # kWh
P_bat_max = 3 # kW
eff = 0.9

#VARIABLES CVXPY
P_bat_ch = cp.Variable(T)
P_bat_dis = cp.Variable(T)
P_grid = cp.Variable(T)
P_pv_curtail = cp.Variable(T, nonneg=True)
SOC = cp.Variable(T+1)

#FORMULATION MATHEMATIQUE
constraints = []
SOC0 = 0.5 * E_bat_max
constraints += [SOC[0] == SOC0]
for t in range(T):
    # Bilan puissance: PV + Grid + Dis = Load + Ch
    constraints += [
    P_pv[t] - P_pv_curtail[t]
    + P_grid[t] + P_bat_dis[t]
    == P_load[t] + P_bat_ch[t],

    P_pv_curtail[t] <= P_pv[t]
]
    # SOC dynamique
    constraints += [SOC[t+1] == SOC[t] + eff*P_bat_ch[t] - P_bat_dis[t]/eff]
    # Limites physiques
    constraints += [SOC[t] >= 0.1*E_bat_max, SOC[t] <= 0.9*E_bat_max]
    constraints += [P_bat_ch[t] >=0, P_bat_ch[t] <= P_bat_max]
    constraints += [P_bat_dis[t] >=0, P_bat_dis[t] <= P_bat_max]
    constraints += [P_grid[t] >=0]

#OBJECTIF: Minimiser coût réseau
objective = cp.Minimize(cp.sum(cp.multiply(price_grid, P_grid)))

#RESOLUTION
prob = cp.Problem(objective, constraints)
prob.solve()
print("Statut :", prob.status)
print("Valeur objectif :", prob.value)

print(f"Coût optimal: ${prob.value:.2f} vs sans batterie: ${np.sum(price_grid * np.maximum(0, P_load-P_pv)):.2f}")
print(f"Économie: {100*(1-prob.value/np.sum(price_grid * np.maximum(0, P_load-P_pv))):.1f}%")

# Plot SOC
plt.plot(SOC.value[:-1]);
print(SOC.value[:-1])
plt.xlabel("Temps (h)")
plt.ylabel("SOC")
plt.title("SOC Batterie optimisé");
plt.show()