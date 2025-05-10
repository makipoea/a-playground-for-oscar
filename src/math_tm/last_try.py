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
    Calcule l'erreur quadratique entre les prédictions et les valeurs réelles,
    en ajoutant un coût pour la répartition des angles modulo pi.
    """
    approx_error = np.sum((approx(x, y, parametre, nb_polynome) - z) ** 2)
    
    # Extraction des angles depuis les paramètres et normalisation modulo pi
    angles = parametre[::(len(parametre) // nb_polynome)] % np.pi
    
    # Trier les angles
    angles_sorted = np.sort(angles)
    
    # Calcul des écarts entre angles consécutifs
    angle_diffs = np.diff(np.append(angles_sorted, angles_sorted[0] + np.pi))
    
    # Espacement idéal entre angles
    ideal_spacing = np.pi / nb_polynome
    
    # Calcul de la variance des espacements
    uniformity_cost = np.var(angle_diffs)
    
    # Normalisation du coût pour être dans [0,2]
    angle_cost = 2 * uniformity_cost / (ideal_spacing ** 2 + 1e-6)
    
    return approx_error + angle_cost
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
        coefficients[0] += adjustment + 0.5
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

"""
if __name__ == "__main__":
    main()

"""


import numpy as np
import numpy.polynomial as npl 
import matplotlib.pyplot as plt 
from shapely.geometry import LineString, Point, Polygon
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import root

def abscisse_line(polynome, theta, integration_step, start=-1.41, end=1.41):
    """
    À partir d'un polynôme, calcule par intégration les abscisses des lignes entre start et end.
    Utilise `scipy.optimize.root` pour trouver les racines de manière numérique.
    Modifie start et end pour être le plus grand intervalle dans [start, end] où le polynôme est positif.
    """
    polynome = npl.Polynomial(polynome)
    #print("polynome = ", polynome)

    # Trouver les racines du polynôme dans [start, end]
    roots = [r.real for r in polynome.roots() if r.imag == 0 and start <= r.real <= end]
    roots = sorted(roots)  # Trier les racines

    # Ajouter start et end aux racines pour définir les intervalles
    intervals = []
    previous = start
    for r in roots:
        intervals.append((previous, r))
        previous = r
    intervals.append((previous, end))

    # Trouver le plus grand intervalle où le polynôme est positif
    max_length = 0
    new_start, new_end = start, end  # Initialisation

    for a, b in intervals:
        # Tester le signe du polynôme au milieu de l'intervalle
        mid = (a + b) / 2
        if polynome(mid) > 0 and (b - a) > max_length:
            max_length = b - a
            new_start, new_end = a, b

    #print(f"Nouvel intervalle où le polynôme est positif : [{new_start}, {new_end}]")

    # Calculer les abscisses dans le nouvel intervalle
    primitive = polynome.integ()
    l_x = [new_start]

    while l_x[-1] < new_end:
        # Fonction pour laquelle on cherche la racine: primitive(x) - primitive(l_x[-1]) - integration_step
        def f(x):
            return primitive(x) - primitive(l_x[-1]) - integration_step

        # Estimation initiale pour la racine
        x0 = l_x[-1] + integration_step  # On commence près de la dernière valeur

        # Utilisation de scipy.optimize.root pour trouver la racine
        sol = root(f, x0, method='hybr')  # Méthode hybride (par défaut)

        if sol.success and new_start <= sol.x[0] <= new_end:
            x_new = sol.x[0]
            l_x.append(x_new)
        else:
            break  # Si la recherche de racine échoue ou sort des limites, on arrête

    return l_x

def rotate(l_x, alpha):
    """
    Pour chaque élément x de la liste l_x, crée deux points (x, -2) et (x, +2),
    les fait tourner d'un angle alpha, et retourne la liste des couples de points tournés.
    
    :param l_x: Liste des abscisses.
    :param alpha: Angle de rotation en radians.
    :return: Liste de couples de points tournés.
    """
    # Matrice de rotation
    rotation_matrix = np.array([
        [np.cos(alpha), -np.sin(alpha)],
        [np.sin(alpha), np.cos(alpha)]
    ])
    
    # Liste pour stocker les couples de points tournés
    rotated_pairs = []
    
    for x in l_x:
        # Points initiaux : (x, -2) et (x, 2)
        point1 = np.array([x, -2])
        point2 = np.array([x, 2])
        
        # Application de la rotation
        rotated_point1 = rotation_matrix @ point1
        rotated_point2 = rotation_matrix @ point2
        
        # Ajout du couple de points tournés à la liste
        rotated_pairs.append((rotated_point1, rotated_point2))
    
    return rotated_pairs

def plot_segments(segments):
    """
    Affiche les segments de ligne représentés par une liste de couples de points.
    
    :param segments: Liste de couples de points (chaque couple représente un segment).
    """
    # Créer une nouvelle figure
    plt.figure()
    
    # Tracer chaque segment
    for (point1, point2) in segments:
        # Extraire les coordonnées x et y des points
        x_values = [point1[0], point2[0]]
        y_values = [point1[1], point2[1]]
        
        # Tracer le segment
        plt.plot(x_values, y_values, marker='o', linestyle='-', color='b')
    
    # Ajouter des labels et un titre
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Segments de ligne tournés')
    plt.grid(True)
    plt.axis('equal')  # Pour que les axes aient la même échelle
    plt.show()



def plot_polynomials(angle_polynome_list, l_lignes, nb_results_points=100):
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
        #print(f"Segments pour le polynôme {i+1} : {l_lignes[i]}")
        for ligne in l_lignes[i]:  
            fig.add_trace(go.Scatter3d(
                x=[ligne[0][0], ligne[1][0]],  # Deux points pour former un segment
                y=[ligne[0][1], ligne[1][1]],
                z=[0, 0],  # Assure-toi que z est bien défin
                mode='lines',
                line=dict(color='blue', width=1)))

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
            title=f'Polynôme {i + 1} (Angle: {angle_phi:.2f})',
            xaxis=dict(range=[0, 1]),
            yaxis=dict(range=[0, 1])
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
        title='Tous les polynômes simultanément',
        xaxis=dict(range=[0, 1]),
        yaxis=dict(range=[0, 1])
    )

    # Afficher la figure
    fig_all.show()

    # Afficher la somme des polynômes et la fonction à approximer
    fig_sum = go.Figure()

    # Ajouter la surface de la somme des polynômes (rouge)
    """
    fig_sum.add_trace(go.Surface(
        x=x,
        y=y,
        z=z_sum,
        colorscale='Reds',  # Palette de couleurs pour la somme
        opacity=0.9,
        name='Somme des polynômes'
    ))
    """
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

    for l_ligne in l_lignes:
        for ligne in l_ligne:  
                fig_sum.add_trace(go.Scatter3d(
                    x=[ligne[0][0], ligne[1][0]],  # Deux points pour former un segment
                    y=[ligne[0][1], ligne[1][1]],
                    z=[0, 0],  # Assure-toi que z est bien défin
                    mode='lines',
                    line=dict(color='blue', width=1)))

    # Configurer la mise en page
    fig_sum.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            #aspectmode='cube',  # Force une boîte carrée
            #aspectratio=dict(x=1, y=1, z=1)
        ),
        margin=dict(l=0, r=0, b=0, t=0),  # Réduire les marges
        width=1000,
        height=1000,
        title='Somme des polynômes (rouge) et fonction à approximer (vert)',
        xaxis=dict(range=[0, 1]),
        yaxis=dict(range=[0, 1])
    )

    # Afficher la figure
    fig_sum.show()

def clip(lines):
    result = []
    for (p1, p2) in lines:
        (x0, y0), (x1, y1) = p1, p2
        dx = x1 - x0
        dy = y1 - y0
        
        # Vérifier si les deux points sont dans le carré
        def inside(p):
            return 0 <= p[0] <= 1 and 0 <= p[1] <= 1
            
        if inside(p1) and inside(p2):
            result.append((p1, p2))
            continue

        # Calcul des intersections avec les 4 bords
        ts = []
        if dx != 0:  # Test bords verticaux
            for x_edge in [0, 1]:
                t = (x_edge - x0) / dx
                y = y0 + t * dy
                if 0 <= y <= 1 and t >= 0 and t <= 1:
                    ts.append((t, (x_edge, y)))
                    
        if dy != 0:  # Test bords horizontaux
            for y_edge in [0, 1]:
                t = (y_edge - y0) / dy
                x = x0 + t * dx
                if 0 <= x <= 1 and t >= 0 and t <= 1:
                    ts.append((t, (x, y_edge)))

        # Ajout des points initiaux s'ils sont dans le carré
        if inside(p1):
            ts.append((-1, p1))  # t=-1 pour être avant toutes les intersections
        if inside(p2):
            ts.append((2, p2))  # t=2 pour être après toutes les intersections

        # Tri des points par paramètre t
        ts.sort()
        
        # Filtrage des intersections valides
        valid = []
        for t, p in ts:
            if 0 <= t <= 1 or p in [p1, p2]:
                valid.append(p)
        
        # Détermination des points de sortie
        if len(valid) >= 2:
            result.append((valid[0], valid[-1]))
        elif len(valid) == 1:
            result.append((valid[0], valid[0]))
    return result

def contraintes(x, y):
    """
    Fonction à approximer.
    """
    #return np.sin(x * 3) * np.cos(y * 3) + 1
    #return (x*x-0.5)*(y-0.5)*2+1
    #return np.sqrt(x*2+y*2)
    #return 1/np.exp((x-0.5)**2+(y-0.5)**2)
    return (x-0.5)*(y-0.5)*2 
def main():
    
    nb_train_points = 10
    nb_results_points = 100
    nb_polynome = 2
    degree = 2
    integration_steps = 0.01

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
    l_poly = angle_polynome_list
    l_lignes = []
    for poly in l_poly:
        l_x = abscisse_line(poly[1], 0, integration_steps)
        l_rot = rotate(l_x, poly[0])
        #print(len(l_x))
        l_clip = clip(l_rot)
        print(len(l_x), len(l_rot), len(l_clip))
        l_lignes.append(l_clip)

    plot_polynomials(l_poly, l_lignes, nb_results_points=100)
    """
    
    poly = [1, 2, 3]
    l_x = abscisse_line(poly, 0, 0.1)
    print(l_x)
    l_droite = rotate(l_x, 0.2)
    plot_segments(clip(l_droite))
    """
    return l_lignes
