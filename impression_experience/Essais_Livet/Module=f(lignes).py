import matplotlib.pyplot as plt 
import csv
import pandas as pd 
from scipy import stats
import numpy as np

fichiers = ["F3.csv","F4C.csv","F5A.csv","F6.csv","F7.csv","F8.csv","F9.csv","F15.csv"]

Pentes=[]
Nombre_ligne=[]

for i in range(len(fichiers)):
    file=fichiers[i]
    if i==7:
        lines_count=15
    else : 
        lines_count=3+i
    Nombre_ligne.append(lines_count)
    dico = dict(pd.read_csv(file, delimiter=";"))

    force = list(dico['charge (N)'])
    deplacement = list(dico['deplacement (mm)'])
    force_droit = []
    deplacement_droit = []
    droit = True
    
    for i in range(len(force)):
        if force[i] > 300 and force[i] < 600 and droit:
            deplacement_droit.append(deplacement[i])
            force_droit.append(force[i])    
        if force[i] > 500: 
            droit = False
    
    

    X = np.array(deplacement_droit)
    Y = np.array(force_droit)
    slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
    Pentes.append(slope*8/5)
    print(Nombre_ligne, Pentes)

plt.scatter(Nombre_ligne,Pentes)
plt.title('Remplissage linéaire : évolution de E en fonction du nombre de lignes')
plt.xlabel('Nombre de lignes')
plt.ylabel('Module de Young en MPa')    
plt.show()