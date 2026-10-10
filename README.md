# Optimisation d'une microgrid avec CVXPY

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1zMkjoeiYlSyddHa6pD0YY1T01zy2TZx9?usp=sharing)

Ce projet modélise et optimise le pilotage d'une microgrid électrique sur 24 heures en minimisant le coût d'achat d'électricité sur le réseau.

## Objectif

Le script utilise `cvxpy` pour déterminer la meilleure stratégie de gestion entre :

- production photovoltaïque,
- consommation locale,
- stockage dans la batterie,
- import/export depuis le réseau,
- éventuel curtailment de la production PV.

L'objectif est de minimiser le coût du réseau tout en respectant les contraintes physiques de la batterie et de la demande.

## Modèle de la microgrid

Le programme prend en compte :

- une production PV synthétique sur 24 heures,
- une charge électrique variable au cours de la journée,
- un prix d'achat de l'électricité sur le réseau variable dans le temps,
- une batterie avec capacité, puissance et rendement limites,
- la dynamique de l'état de charge (SOC).

## Fichiers

- `microgrid_optimization_cvxpy.py` : script principal d'optimisation,
- `microgrid_optimization_cvxpy.ipynb` : version notebook pour exploration visuelle,
- `requirements.txt` : dépendances Python du projet.

## Prérequis

Python 3.9+ et les dépendances suivantes :

```bash
pip install -r requirements.txt
```

## Exécution

```bash
python microgrid_optimization_cvxpy.py
```

Le script affiche :

- le statut de l'optimisation,
- la valeur objective,
- le coût optimal comparé à un cas sans batterie,
- le gain économique obtenu,
- un graphique du niveau de charge de la batterie (SOC).

## Exemple de sortie

Le programme produit une optimisation linéaire du type :

- minimisation du coût réseau,
- contraintes de bilan de puissance,
- contraintes de capacité et de limite de puissance de la batterie,
- état de charge dynamique sur la journée.
