import numpy as np
from scipy.optimize import minimize 
import matplotlib.pyplot as plt
import random as rd

nb_train_points = 10
nb_results_points = 100
nb_courbe=2
degre = 2

def phi(x, y, parametre):
    """
    parametre : Angle, a0 + a1x + a2x2 ...
    """
    r = np.sqrt(x**2+y**2)
    theta = np.arctan2(y , x)
    s = 0
    theta_1 = parametre[0]  
    for i, a in enumerate(parametre[1:]): 
        s += a * (r * np.cos(theta - theta_1))**i
    return s

def approx(x, y, parametre):
    so = 0
    p = np.split(parametre, nb_courbe)
    for i in range(nb_courbe):
        so += phi(x, y, p[i]) 
    return so

def contraintes(x, y):
    #return 3*x*y
    return (x-0.5)*(y-0.5)

x_contraintes = [] #;np.linspace(-1, 1, 10)
y_contraintes = [] #np.linspace(-1, 1, 10)


for x in range(nb_train_points):
    for y in range(nb_train_points):
        x_contraintes.append(x/nb_train_points)
        y_contraintes.append(y/nb_train_points)

x_contraintes = np.array(x_contraintes)
y_contraintes = np.array(y_contraintes)
z_contraintes = np.array(list(map(contraintes, x_contraintes, y_contraintes)))

def error(parametre):
    return np.sum((approx(x_contraintes, y_contraintes, parametre)-z_contraintes)**2)

parametre_initiaux = np.array([np.random.uniform(0, 4) for _ in range(((degre+2)*nb_courbe))])#np.array([0]*(degre+2)*nb_courbe)# np.random.randn((degre + 2) * nb_courbe)


coeff = minimize(error, parametre_initiaux).x

print(np.split(coeff, nb_courbe))

x_results = []
y_results = []


for x in range(nb_results_points):
    for y in range(nb_results_points):
        x_results.append(x/nb_results_points)
        y_results.append(y/nb_results_points)

x_results = np.array(x_results)
y_results = np.array(y_results)

z_results = approx(x_results, y_results, coeff)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


ax.scatter(x_contraintes, y_contraintes, z_contraintes, color='green', s=10)
ax.scatter(x_results, y_results, z_results, color='red', s=1)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()