import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os
from scipy import stats

def calculate_stiffness(file):
    lire=dict(pd.read_csv(file,delimiter=";"))
    force = list(lire["charge (N)"])
    deplacement = list(lire["deplacement (mm)"])
    force_reg=[]
    deplacement_reg=[]
    droit = True
    for i in range(len(force)):
            if ((deplacement[i] > 2.3 and deplacement[i] < 4.1) or force[i]>200 ) and droit:
                deplacement_reg.append(deplacement[i])
                force_reg.append(force[i]) 
            if deplacement[i]>4.1 or i==len(deplacement)-1 or force[i]>force[i+1]+5: droit = False

    X = np.array(deplacement_reg)
    Y = np.array(force_reg)
    slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y) 
    return slope

def plot_Young_Mass():
    directories = ['Eprouvette','Eprouvette_lignes_peu_dense','Eprouvette_lignes_dense']
    Youngs_constant=[]
    Masses_constant=[]
    Youngs_variable=[]
    Masses_variable=[]
    for directory in directories:
        L=os.listdir(directory)
        os.chdir(directory)
        Dmass=dict(pd.read_csv("masse.txt",delimiter=";"))
        for file in L:
            if file!="masse.txt" and file!="constant.csv":
                young = calculate_stiffness(file)
                mass= float(list(Dmass[file[:-4]])[0])
                if file[:8]=="variable":
                    Masses_variable.append(mass)
                    Youngs_variable.append(young)
                else :
                    Masses_constant.append(mass)
                    Youngs_constant.append(young)
        os.chdir("..")
    
    plt.scatter(Masses_constant,Youngs_constant, label = "remplissage lineaire", color = 'blue')
    plt.scatter(Masses_variable,Youngs_variable, label = "remplissage variable" , color = 'red')
    plt.xlabel("masse (g)")
    plt.ylabel("Raideur (N/mm)")
    plt.legend()
    plt.title("Comparaison éprouvettes en remplissage linéaire")
    plt.show()


plot_Young_Mass()