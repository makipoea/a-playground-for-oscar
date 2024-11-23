import matplotlib.pyplot as plt 
import csv
import pandas as pd 
from scipy import stats
import numpy as np

name_file = ['F15.csv', 'F4A.csv', 'F4C.csv', 'F6.csv', 'F8.csv', 'OA3.csv', 'OA5.csv', 'OA7.csv', 'OB35.csv', 'F3.csv', 'F4B.csv', 'F5A.csv', 'F7.csv', 'F9.csv', 'OA4.csv', 'OA6.csv', 'OB34.csv', 'OB37.csv']

for file in name_file:

    dico = dict(pd.read_csv(file, delimiter=";"))

    force = list(dico['charge (N)'])
    deplacement = list(dico['deplacement (mm)'])
    force_droit = []
    deplacement_droit = []
    droit = True
    
    for i in range(len(force)):
        if force[i] > 100 and force[i] < 500 and droit:
            deplacement_droit.append(deplacement[i])
            force_droit.append(force[i])    
        if force[i] > 500: 
            droit = False
    
    plt.plot(deplacement_droit, force_droit)

    X = np.array(deplacement_droit)
    Y = np.array(force_droit)
    slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
    print(slope*(8/5))
    
plt.show()