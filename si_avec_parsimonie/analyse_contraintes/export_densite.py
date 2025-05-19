import pyvista as pv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import json 
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import sympy as sp

def teste(filename="eprouvette.vtu"):
    # Charger le fichier VTU
    mesh = pv.read(filename)

    ##Afficher les informations du maillage
    print(mesh)

    ##affiche la maille en 3d avec un gradient de couleur pour representer la contrainte (un peu comme sur fusion)
    mesh.plot(scalars='Contrainte:Normale XX',component=0, cmap='turbo', cpos='xy') 

    ##Extraction de la contrainte sigmaXX
    lXX= mesh.point_data['Contrainte:Normale XX']
    print(lXX)

    ##Extraction des coordonées des points 
    pts = mesh.points
    print(pts)

def contraintes_to_densite(l_contrainte):
    l_contrainte = np.array(l_contrainte)
    return (l_contrainte-min(l_contrainte))/(max(l_contrainte)-min(l_contrainte))

def read_file(file):
    mesh = pv.read(file)
    lcontrainte= mesh.point_data['Contrainte:von Mises']
    l_densite = contraintes_to_densite(lcontrainte)
    l_points = mesh.points.tolist()
    l_points = [tuple(point) for point in l_points] # pour pouvoir les passer en clé de dictionnaire 

    return l_points, l_densite


def compute_densite(file):
    mesh = pv.read(file)
    lcontrainte= mesh.point_data['Contrainte:von Mises']
    l_densite = contraintes_to_densite(lcontrainte)
    l_points = mesh.points.tolist()
    l_points = [tuple(point) for point in l_points] # pour pouvoir les passer en clé de dictionnaire 
    
    densite_dico = dict(zip(l_points, l_densite))
    #Ldens = set_density(dmin,dmax,Lstress,fct)
    return densite_dico.copy()

def compute_polynome(l_points, l_densite, degree=2):
    """
    retourne les coefficient du polynome a 3 inconnues obtenue par methode des moindre carré :
    P(X, Y, Z) = densité
    """
    # Générer les termes polynomiaux
    poly = PolynomialFeatures(degree=degree)
    P_poly = poly.fit_transform(l_points)

    # Ajuster le modèle linéaire (sur les termes polynomiaux)
    model = LinearRegression()
    model.fit(P_poly, l_densite)

    return model, poly
    


def plot_predictions_3d(l_points, l_densite, model, poly, feature_names):
    X = np.array(l_points)
    y_true = np.array(l_densite)

    # Prédictions
    X_poly = poly.transform(X)
    y_pred = model.predict(X_poly)

    fig = plt.figure(figsize=(14, 6))
    ax1 = fig.add_subplot(131, projection='3d')
    ax2 = fig.add_subplot(132, projection='3d')
    ax3 = fig.add_subplot(133, projection='3d')

    # Nuage original
    ax1.scatter(X[:, 0], X[:, 1], X[:, 2], c=y_true, cmap='viridis')
    ax1.set_title("Données originales")
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_zlabel('z')

    # Nuage prédit
    ax2.scatter(X[:, 0], X[:, 1], X[:, 2], c=y_pred, cmap='plasma')
    ax2.set_title("Prédictions du polynôme")
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_zlabel('z')

    # Erreur absolue
    ax3.scatter(X[:, 0], X[:, 1], X[:, 2], c=np.abs(y_true - y_pred), cmap='inferno')
    ax3.set_title("Erreur absolue")
    ax3.set_xlabel('x')
    ax3.set_ylabel('y')
    ax3.set_zlabel('z')

    plt.tight_layout()
    plt.show()

    # Afficher les coefficients du polynôme
    print("\n--- Polynôme ajusté ---")
    for coef, name in zip(model.coef_, feature_names):
        print(f"{coef:+.4f} * {name}")
    print(f"{model.intercept_:+.4f} (intercept)")

    
import numpy as np
from sklearn.preprocessing import PolynomialFeatures

def polynomial_to_tensor(model, poly, var_names=['x', 'y', 'z']):
    """
    Convertit un polynôme sklearn en un tableau 3D où tab[i][j][k] correspond au coeff de x^i * y^j * z^k.
    
    :param model: modèle sklearn entraîné (LinearRegression)
    :param poly: objet PolynomialFeatures utilisé pour générer les termes
    :param var_names: noms des variables, par défaut ['x', 'y', 'z']
    :return: tableau numpy 3D
    """
    from collections import defaultdict

    coef_dict = defaultdict(float)
    feature_names = poly.get_feature_names_out(var_names)

    max_deg = poly.degree
    # Remplir le dictionnaire des coefficients
    for coef, name in zip(model.coef_, feature_names):
        if name == "1":
            i = j = k = 0
        else:
            parts = name.replace("^", "**").split(" ")
            i = j = k = 0
            for part in parts:
                if part.startswith("x"):
                    i += int(part.split("**")[1]) if "**" in part else 1
                elif part.startswith("y"):
                    j += int(part.split("**")[1]) if "**" in part else 1
                elif part.startswith("z"):
                    k += int(part.split("**")[1]) if "**" in part else 1
        coef_dict[(i, j, k)] += coef

    # Créer le tableau 3D
    tab = np.zeros((max_deg + 1, max_deg + 1, max_deg + 1))
    for (i, j, k), val in coef_dict.items():
        tab[i][j][k] = val

    # Ajouter l’intercept à (0,0,0)
    tab[0][0][0] += model.intercept_

    return tab

def save_polynme_as_json(tensor, l_points, filename):
    """
    tensor : polynome sous forme de tensseur 
    -> exporte le polynome pour que ce dernier soit accessible par le programme C++
    """
    x_coords = [p[0] for p in l_points]
    y_coords = [p[1] for p in l_points]
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    
    b_box = [[min_x, min_y], [max_x, min_y], [max_x, max_y], [min_x, max_y]]
    print(b_box)
    data = {
        "tensor": tensor.tolist(),
        "bbox": b_box
    }

    # Écriture dans le fichier JSON
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def plot_polynomial_slices(model, poly, points, n_slices=5, grid_size=50):
    """
    Affiche des surfaces 3D de P(X, Y, Z=z) pour z équi-répartis sur la hauteur de la pièce.
    
    :param model: modèle sklearn entraîné (LinearRegression)
    :param poly: objet PolynomialFeatures utilisé pour générer les termes
    :param points: liste de tuples (x, y, z) des points d'origine
    :param n_slices: nombre de tranches le long de Z
    :param grid_size: résolution du maillage X-Y
    """
    # Extraction des bornes de la pièce
    pts = np.array(points)
    x_min, x_max = pts[:,0].min(), pts[:,0].max()
    y_min, y_max = pts[:,1].min(), pts[:,1].max()
    z_min, z_max = pts[:,2].min(), pts[:,2].max()
    
    # Valeurs de z à tracer
    zs = np.linspace(z_min, z_max, n_slices)
    
    fig = plt.figure(figsize=(4 * n_slices, 4))
    for idx, z in enumerate(zs, 1):
        # Construction de la grille XY
        xs = np.linspace(x_min, x_max, grid_size)
        ys = np.linspace(y_min, y_max, grid_size)
        X, Y = np.meshgrid(xs, ys)
        
        # Prépare les points pour la prédiction
        XY_flat = np.column_stack([X.ravel(), Y.ravel(), np.full(X.size, z)])
        XY_poly = poly.transform(XY_flat)
        Z_pred = model.predict(XY_poly).reshape(X.shape)
        
        # Plot
        ax = fig.add_subplot(1, n_slices, idx, projection='3d')
        surf = ax.plot_surface(X, Y, Z_pred, cmap='viridis', edgecolor='none')
        ax.set_title(f"Z = {z:.2f}")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Density')
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    teste("tor.vtu")
    l_points, l_densite = read_file('tor.vtu')
    print(min(l_densite), max(l_densite))

    model, poly = compute_polynome(l_points, l_densite, degree=5)
    feature_names = poly.get_feature_names_out(['x', 'y', 'z'])
    tableau_coeff = polynomial_to_tensor(model, poly)
    print(tableau_coeff)
    print(tableau_coeff[1])
    
    save_polynme_as_json(tableau_coeff, l_points,"polynome.json")
    plot_polynomial_slices(model, poly, l_points)
    plot_predictions_3d(l_points, l_densite, model, poly, feature_names)
