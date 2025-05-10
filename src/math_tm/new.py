import numpy as np
from scipy.optimize import minimize
import plotly.graph_objects as go

def phi(x, y, parametre):
    """
    Évalue un polynôme en un point (x, y).
    """
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    s = 0
    theta_1 = parametre[0]
    for i, a in enumerate(parametre[1:]):
        s += a * (r * np.cos(theta - theta_1))**i
    return s

def approx(x, y, parametre, nb_polynome):
    """
    Calcule la somme des polynômes en un point (x, y).
    """
    so = 0
    p = np.split(parametre, nb_polynome)
    for i in range(nb_polynome):
        so += phi(x, y, p[i])
    return so

def error(parametre, x, y, z, nb_polynome):
    """
    Calcule l'erreur quadratique entre les prédictions et les valeurs réelles.
    """
    return np.sum((approx(x, y, parametre, nb_polynome) - z)**2)

def decompose(target_point, nb_polynome, degree):
    """
    Décompose les points en polynômes.
    """
    parametre_initiaux = np.array([np.random.uniform(0, 4) for _ in range(((degree + 2) * nb_polynome))])

    x = np.array([point[0] for point in target_point])
    y = np.array([point[1] for point in target_point])
    z = np.array([point[2] for point in target_point])

    parametre_finaux = np.array(minimize(lambda parameter: error(parameter, x, y, z, nb_polynome), parametre_initiaux).x)
    liste_param = np.split(parametre_finaux, nb_polynome)
    coeff = []
    angle = []
    for p in liste_param:
        p = list(p)
        angle.append(p.pop(0))
        coeff.append(p)

    return parametre_finaux, angle, coeff

def contraintes(x, y):
    """
    Fonction à approximer.
    """
    return np.sin(x * 3) * np.cos(y * 3) + 1

def plot_polynomials(angle_polynome_list, nb_results_points=100):
    """
    Affiche les polynômes individuellement, simultanément, et la somme des polynômes.
    """
    # Générer une grille de points (x, y)
    x = np.linspace(0, 1, nb_results_points)
    y = np.linspace(0, 1, nb_results_points)
    x, y = np.meshgrid(x, y)

    # Initialiser la somme des polynômes
    z_sum = np.zeros_like(x)

    # Liste des couleurs pour chaque polynôme
    colorscales = ['Viridis', 'Plasma', 'Inferno', 'Magma', 'Cividis']

    # Afficher chaque polynôme dans une fenêtre séparée
    for i, (angle_phi, coefficients) in enumerate(angle_polynome_list):
        # Calculer les valeurs z du polynôme
        z = phi(x, y, [angle_phi] + coefficients)

        # Créer une figure Plotly pour ce polynôme
        fig = go.Figure()

        # Ajouter la surface du polynôme
        fig.add_trace(go.Surface(
            x=x,
            y=y,
            z=z,
            colorscale=colorscales[i % len(colorscales)],  # Palette de couleurs
            opacity=0.7,
            name=f'Polynôme {i + 1} (Angle: {angle_phi:.2f})'
        ))

        # Configurer la mise en page
        fig.update_layout(
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z',
                aspectmode='cube',  # Force une boîte carrée
                aspectratio=dict(x=1, y=1, z=1)
            ),
            margin=dict(l=0, r=0, b=0, t=0),  # Réduire les marges
            width=1000,
            height=1000,
            title=f'Polynôme {i + 1} (Angle: {angle_phi:.2f})'
        )

        # Afficher la figure
        fig.show()

        # Ajouter à la somme totale
        z_sum += z

    # Afficher tous les polynômes simultanément dans une seule fenêtre
    fig_all = go.Figure()

    for i, (angle_phi, coefficients) in enumerate(angle_polynome_list):
        # Calculer les valeurs z du polynôme
        z = phi(x, y, [angle_phi] + coefficients)

        # Ajouter la surface du polynôme
        fig_all.add_trace(go.Surface(
            x=x,
            y=y,
            z=z,
            colorscale=colorscales[i % len(colorscales)],  # Palette de couleurs
            opacity=0.7,
            name=f'Polynôme {i + 1} (Angle: {angle_phi:.2f})'
        ))

    # Configurer la mise en page
    fig_all.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='cube',  # Force une boîte carrée
            aspectratio=dict(x=1, y=1, z=1)
        ),
        margin=dict(l=0, r=0, b=0, t=0),  # Réduire les marges
        width=1000,
        height=1000,
        title='Tous les polynômes simultanément'
    )

    # Afficher la figure
    fig_all.show()

    # Afficher la somme des polynômes et la fonction à approximer
    fig_sum = go.Figure()

    # Ajouter la surface de la somme des polynômes (rouge)
    fig_sum.add_trace(go.Surface(
        x=x,
        y=y,
        z=z_sum,
        colorscale='Reds',  # Palette de couleurs pour la somme
        opacity=0.9,
        name='Somme des polynômes'
    ))

    # Ajouter la surface de la fonction à approximer (vert)
    z_contraintes = contraintes(x, y)
    fig_sum.add_trace(go.Surface(
        x=x,
        y=y,
        z=z_contraintes,
        colorscale='Greens',  # Palette de couleurs pour la fonction à approximer
        opacity=0.7,
        name='Fonction à approximer'
    ))

    # Configurer la mise en page
    fig_sum.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='cube',  # Force une boîte carrée
            aspectratio=dict(x=1, y=1, z=1)
        ),
        margin=dict(l=0, r=0, b=0, t=0),  # Réduire les marges
        width=1000,
        height=1000,
        title='Somme des polynômes (rouge) et fonction à approximer (vert)'
    )

    # Afficher la figure
    fig_sum.show()

def find_minimum_on_unit_square(polynomial, angle, coefficients):
    """
    Trouve le minimum d'un polynôme sur le carré [0, 1]².
    """
    def objective(params):
        x, y = params
        return phi(x, y, [angle] + coefficients)

    # Initialisation de la recherche du minimum
    bounds = [(0, 1), (0, 1)]
    result = minimize(objective, x0=[0.5, 0.5], bounds=bounds)
    return result.fun

def find_global_minimum(angle_polynome_list):
    """
    Trouve le minimum global de tous les polynômes sur le carré [0, 1]².
    """
    global_min = float('inf')  # Initialisation avec une valeur infinie

    for angle, coefficients in angle_polynome_list:
        # Trouver le minimum du polynôme courant
        min_value = find_minimum_on_unit_square(phi, angle, coefficients)
        # Mettre à jour le minimum global
        if min_value < global_min:
            global_min = min_value

    return global_min

def adjust_constant_terms(angle_polynome_list, adjustment):
    """
    Ajuste uniquement les termes constants des polynômes en ajoutant une valeur donnée.
    """
    adjusted_list = []
    for angle, coefficients in angle_polynome_list:
        # Ajouter l'ajustement uniquement au terme constant (premier coefficient)
        coefficients[0] += adjustment
        adjusted_list.append((angle, coefficients))
    return adjusted_list




def main():
    nb_train_points = 10
    nb_results_points = 100
    nb_polynome = 3
    degree = 4

    # Générer les points d'entraînement
    x_contraintes = np.linspace(0, 1, nb_train_points)
    y_contraintes = np.linspace(0, 1, nb_train_points)
    x_contraintes, y_contraintes = np.meshgrid(x_contraintes, y_contraintes)
    x_contraintes = x_contraintes.flatten()
    y_contraintes = y_contraintes.flatten()
    z_contraintes = contraintes(x_contraintes, y_contraintes)

    # Décomposer les points en polynômes
    p, a, c = decompose(list(zip(x_contraintes, y_contraintes, z_contraintes)), nb_polynome, degree)

    # Créer la liste des polynômes avec leurs angles et coefficients
    angle_polynome_list = list(zip(a, c))

    # Trouver le minimum global de tous les polynômes
    global_min = find_global_minimum(angle_polynome_list)

    # Ajuster les termes constants si le minimum global est négatif
    if global_min < 0:
        adjustment = abs(global_min)
        angle_polynome_list = adjust_constant_terms(angle_polynome_list, adjustment)

    # Afficher les polynômes ajustés et leur somme
    plot_polynomials(angle_polynome_list)

if __name__ == "__main__":
    main()