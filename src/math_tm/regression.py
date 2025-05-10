import numpy as np
from scipy.optimize import minimize 
import matplotlib.pyplot as plt
import random as rd


import plotly.graph_objects as go
import numpy as np


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

def approx(x, y, parametre, nb_polynome):
    """
    liste des resulatat de l'aproximation au point x, y
    """
    so = 0
    p = np.split(parametre, nb_polynome)
    for i in range(nb_polynome):
        so += phi(x, y, p[i]) 
    return so

def error(parametre, x, y, z, nb_polynome):
    """
    parametre : liste des coefficent 
    -> erreur absolue avec les points de controle 
    """
    return np.sum((approx(x, y, parametre, nb_polynome)-z)**2)

def decompose(target_point, nb_polynome, degree):
    """
    target_point : list[(x:float, y:float, contriants:float)]
    nb_polynome : int 
    degree : int    
    -> 
    parameter_fianaux  : list[<float>]
    angle : list[<float>]
    coeff :   list[list <float>]
    """
    parametre_initiaux = np.array([np.random.uniform(0, 4) for _ in range(((degree+2)*nb_polynome))])

    x = np.array([point[0] for point in target_point])
    y = np.array([point[1] for point in target_point])
    z = np.array([point[2] for point in target_point])
    
    parametre_finaux = np.array(minimize(lambda parameter:error(parameter, x, y, z, nb_polynome), parametre_initiaux).x)
    liste_param = np.split(parametre_finaux, nb_polynome)
    coeff = []
    angle = []
    for p in liste_param:
        p = list(p)
        angle.append(p.pop(0))
        coeff.append(p)

    return parametre_finaux , angle, coeff


def contraintes(x, y):
    #return 3*x*y
    #return (x-0.5)*(y-0.5)
    return np.sin(x*3)*np.cos(y*3)+1
    #return (x-0.5)**2*y + 3*x*y



def main():
    
    nb_train_points = 10
    nb_results_points = 100
    nb_polynome = 3
    degree = 4
    
    x_contraintes = [] #;np.linspace(-1, 1, 10)
    y_contraintes = [] #np.linspace(-1, 1, 10)


    for x in range(nb_train_points):
        for y in range(nb_train_points):
            x_contraintes.append(x/nb_train_points)
            y_contraintes.append(y/nb_train_points)

    x_contraintes = np.array(x_contraintes)
    y_contraintes = np.array(y_contraintes)
    z_contraintes = np.array(list(map(contraintes, x_contraintes, y_contraintes)))

    
    p, a, c = decompose(list(zip(x_contraintes, y_contraintes, z_contraintes)), nb_polynome, degree)


    x_results = []
    y_results = []


    for x in range(nb_results_points):
        for y in range(nb_results_points):
            x_results.append(x/nb_results_points)
            y_results.append(y/nb_results_points)

    x_results = np.array(x_results)
    y_results = np.array(y_results)

    z_results = approx(x_results, y_results, p, nb_polynome)


    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    ax.scatter(x_contraintes, y_contraintes, z_contraintes, color='green', s=10)
    ax.scatter(x_results, y_results, z_results, color='red', s=1)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()
    """

    fig = go.Figure()

# Ajouter les points des contraintes
    fig.add_trace(go.Scatter3d(
        x=x_contraintes,
        y=y_contraintes,
        z=z_contraintes,
        mode='markers',
        marker=dict(
            size=5,
            color='green',
            opacity=0.8
        ),
        name='Contraintes'
    ))

    # Ajouter les points des résultats
    fig.add_trace(go.Scatter3d(
        x=x_results,
        y=y_results,
        z=z_results,
        mode='markers',
        marker=dict(
            size=3,
            color='red',
            opacity=0.8
        ),
        name='Résultats'
    ))

    # Configurer les axes
    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
        margin=dict(l=0, r=0, b=0, t=0)  # Réduire les marges
    )

    # Afficher la figure
    fig.show()
    """
if __name__ == "__main__":
    main()