import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os
from scipy import stats
"""file = "AAA1.csv"

dico= dict(pd.read_csv(file,delimiter=";"))
force = list(dico["charge (N)"])
deplacement = list(dico["deplacement (mm)"])

plt.plot(np.array(deplacement),np.array(force))
plt.show()"""

colors=['blue','red','green','yellow','purple','black','orange','brown','cyan']

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


def comparatif(folder) :
    path=folder
    files=os.listdir(path)
    os.chdir(folder)
    dico=dict(pd.read_csv("masse.txt",delimiter=";"))
    fig , ax = plt.subplots()
    i=0
    xmin=-0.1
    xmax=0
    anotations=[]
    for file in files:
        if file!="masse.txt":
            raid = round(calculate_stiffness(file),2)
            print('Raideur de '+file[:-4]+' : ', raid, 'N/mm')
            lire=dict(pd.read_csv(file,delimiter=";"))
            force = list(lire["charge (N)"])
            deplacement = list(lire["deplacement (mm)"])
            ax.plot(np.array(deplacement),np.array(force), label = file[:-4]+" : "+str(list(dico[file[:-4]])[0])+" g" , color = colors[i])
            an=ax.annotate(
                    'Rupture : '+str(deplacement[-1])+' mm'+'\n'+str(force[-1])+" N"+"\n"+'Raideur : '+str(raid)+' N/mm',
                    xy=(deplacement[-1],force[-1]), xycoords='data',
                    xytext=(30*(i+1), -40*(i+1)), textcoords='offset points',
                    bbox=dict(boxstyle="round", fc="0.8",color = colors[i]),
                    arrowprops=dict(arrowstyle="->",
                    connectionstyle="angle,angleA=0,angleB=90,rad=10"))
            anotations.append(an)
            an.draggable()
            if deplacement[-1]>xmax : xmax = deplacement[-1]
            i+=1
    ax.set_xlim(xmin,xmax+3)
    ax.set_xlabel("deplacement (mm)")
    ax.set_ylabel('force (N)')
    ax.legend()
    ax.set_title('Comparaison des éprouvettes '+folder)
    plt.show()

comparatif('Eprouvette_lignes_dense')




            