import matplotlib.pyplot as plt 
import csv
import pandas as pd 
from scipy import stats
import numpy as np

name_file = ['F15.csv', 'F4A.csv', 'F4C.csv', 'F6.csv', 'F8.csv', 'OA3.csv', 'OA5.csv', 'OA7.csv', 'OB35.csv', 'F3.csv', 'F4B.csv', 'F5A.csv', 'F7.csv', 'F9.csv', 'OA4.csv', 'OA6.csv', 'OB34.csv', 'OB37.csv']


name_file_oscar = ['OA3.csv', 'OA4.csv', 'OA5.csv', 'OA6.csv', 'OA7.csv']

value = [(3, 5), (3, 5), (2, 5), (0, 2.5), (5, 7.5)]

masse_oscar = [4.83, 6.03, 7.26, 9.75, 13]

"""
Arbre / masse en g  
3: 4.83
4: 6.03
5: 7.26
6: 9.75
7: 13.00
breche 
37: 7.34
35: 8.09
34: 8.24
"""


def afficher_pentes(fich=name_file):
    for file in fich:

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
        print(file,slope*(8/5))
    plt.show()
#afficher_pentes()

def Young_masse():
    fichF,massF=['F3.csv','F4B.csv','F5A.csv','F6.csv','F7.csv','F8.csv','F9.csv','F15.csv'],[5.02,5.28,5.75,6.07,6.52,6.77,7.16,8.8]
    for k in range(len(massF)) :
        dico = dict(pd.read_csv(fichF[k], delimiter=";"))

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

        X = np.array(deplacement_droit)
        Y = np.array(force_droit)
        slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
        plt.scatter([massF[k]],[slope*8/5],label=fichF[k])
    
    fichO,massO=['OA3.csv','OA4.csv','OA5.csv','OA6.csv','OA7.csv'],[2,2.26,2.72,3.61,5.41]
    for k in range(len(massO)) :
        dico = dict(pd.read_csv(fichO[k], delimiter=";"))

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

        X = np.array(deplacement_droit)
        Y = np.array(force_droit)
        slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
        plt.scatter([massO[k]],[slope*8/5],marker='x',label=fichO[k])

    plt.legend()

    plt.title('Module de Young et masse')
    plt.xlabel('masse en g')
    plt.ylabel('module de Young en  MPa')

    plt.show()


def oscar():
    l_slope = []
    fig , ax = plt.subplots()

    for n_file, file in enumerate(name_file_oscar):
        dico = dict(pd.read_csv(file, delimiter=";"))

        for i in range(len(force)):
            if force[i] > 100 and force[i] < 500 and droit:
                deplacement_droit.append(deplacement[i])
                force_droit.append(force[i])    
            if force[i] > 500: 
                droit = False

        X = np.array(deplacement_droit)
        Y = np.array(force_droit)
        slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
        plt.scatter([massF[k]],[slope*8/5],label=fichF[k])
    
    fichO,massO=['OA3.csv','OA4.csv','OA5.csv','OA6.csv','OA7.csv'],[2,2.26,2.72,3.61,5.41]
    for k in range(len(massO)) :
        dico = dict(pd.read_csv(fichO[k], delimiter=";"))


        force = list(dico['charge (N)'])
        deplacement = list(dico['deplacement (mm)'])
        force_droit = []
        deplacement_droit = []
        droit = True

        
        for i in range(len(force)):
            if deplacement[i]<value[n_file][1] and deplacement[i]>value[n_file][0]:
                deplacement_droit.append(deplacement[i])
                force_droit.append(force[i])    
        
        
        X = np.array(deplacement_droit)
        Y = np.array(force_droit)

        slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
        l_slope.append(slope)
    
        #ax.plot(X, Y, color=[n_file/5, (5-n_file)/5, 0.3], label=file)

    #plt.scatter(list(range(len(masse_oscar))), l_slope)
    plt.plot(masse_oscar, l_slope)

    plt.show()

def same_curve():
    l_slope = []
    file_name = ["F4A.csv", "F4B.csv", "F4C.csv"]
    for n_file, file in enumerate(file_name):
        
        dico = dict(pd.read_csv(file, delimiter=";"))
        force = list(dico['charge (N)'])
        deplacement = list(dico['deplacement (mm)'])
        force_droit = []
        deplacement_droit = []

        for dep, fo in zip(deplacement, force):
            if dep<3 and dep>2.5:
                deplacement_droit.append(dep)
                force_droit.append(fo)

        X = np.array(deplacement_droit)
        Y = np.array(force_droit)

        slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
        l_slope.append(slope)

    print(l_slope)

    plt.show()


    
        for i in range(len(force)):
            if force[i] > 100 and force[i] < 500 and droit:
                deplacement_droit.append(deplacement[i])
                force_droit.append(force[i])    
            if force[i] > 500: 
                droit = False

        X = np.array(deplacement_droit)
        Y = np.array(force_droit)
        slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
        plt.scatter([massO[k]],[slope*8/5],marker='x',label=fichO[k])

    plt.legend()

    plt.title('Module de Young et masse')
    plt.xlabel('masse en g')
    plt.ylabel('module de Young en  MPa')

    plt.show()
Young_masse()

