import pyvista as pv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Charger le fichier VTU
#mesh = pv.read('resultat.vtu')

##Afficher les informations du maillage
#print(mesh)

##affiche la maille en 3d avec un gradient de couleur pour representer la contrainte (un peu comme sur fusion)
#mesh.plot(scalars='Contrainte:Normale XX',component=0, cmap='turbo', cpos='xy') 

##Extraction de la contrainte sigmaXX
#lXX= mesh.point_data['Contrainte:Normale XX']
#print(lXX)

##Extraction des coordonées des points 
#pts = mesh.points
#print(pts)

def coupe(lcontrainte,lpoints,zo=4) :   #affiche un graphe 3D representant la contrainte en foction du point (x,y) d'une coupe sur le plan (z=zo)
    Lx,Ly,Lstress= [],[],[]
    for i in range(len(lcontrainte)) :
        if lpoints[i][2]==zo:                       
            Lx.append(lpoints[i][0])
            Ly.append(lpoints[i][1])
            Lstress.append(lcontrainte[i])


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(Lx, Ly, Lstress)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('Contrainte normalle sigmaXX')

    plt.show()

def set_density(dmin,dmax,lcontrainte,fct): #détermine la densité du remplissage en fonction de la contrainte selon une fonction de gradient fct la densité et comprise entre dmin et dmax (flottant entre 0 et 1)
    n=len(lcontrainte)
    stressmin, stressmax= min(lcontrainte) , max(lcontrainte)
    Ldens=[]
    for i in range(n) :
        Ldens.append(fct(dmin,dmax,stressmin,stressmax,lcontrainte[i]))
    return Ldens

def affine(dmin,dmax,stressmin,stressmax,stress) :      #fonction gradient affine
    return dmin + ((stress-stressmin)/(stressmax - stressmin))*(dmax-dmin)


def densite_coupe(file,zo,dmin,dmax,fct): #Genere le trio (liste abscisse, liste ordonees , liste densité) sur un coupe (z=zo) selon les densité min et max voulues et la fonction gradient souhaité
    mesh = pv.read(file)
    lcontrainte= mesh.point_data['Contrainte:Normale XX']
    lpoints = mesh.points
    Lx,Ly,Lstress= [],[],[]
    for i in range(len(lcontrainte)) :
        if lpoints[i][2]==zo:                       
            Lx.append(lpoints[i][0])
            Ly.append(lpoints[i][1])
            Lstress.append(lcontrainte[i])
    Ldens = set_density(dmin,dmax,Lstress,fct)
    return Lx,Ly,Ldens


data= densite_coupe('resultat.vtu',4,0,1,affine)
points=[[data[0][i],data[1][i],0] for i in range(len(data[0]))]
mesh= pv.PolyData(points)
mesh.point_data['density']= data[2]
mesh.plot(scalars='density',component=0, cmap='coolwarm', cpos='xy')