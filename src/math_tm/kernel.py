import numpy as np
import shapely.geometry as sh
import plotly as pl 
import plotly.graph_objects as go
#import pyvista as pv
from last_try import main
from tqdm import tqdm


def resize(kernel, area):
    """
    resize kernel to have area requested
    """
    kernel = np.array(kernel)
    return np.sqrt(area/sh.Polygon(kernel).area)*kernel

def density(x, y, kernel, infill):
    """
    kernel : list[int] supposé centré en 0    
    x, y : int, int, point ou est calculer la densité 
    infill :list[list[int]] liste des courbe polygonales de remplissage
    Area : on modifie le kernel pour qu'il ai l'aire shouaiter
    """

    kernel = np.array(kernel)
    kernel = sh.Polygon(kernel+[x, y])

    length = 0 

    for line in infill:
        line = sh.LineString(line)
        intersection = line.intersection(kernel)
        if not intersection.is_empty:
            length += intersection.length

    return length/kernel.area

kernel = [
    (1.0, 0.0),
    (0.5, 0.8660254037844386),
    (-0.5, 0.8660254037844386),
    (-1.0, 1.2246467991473532e-16),
    (-0.5, -0.8660254037844386),
    (0.5, -0.8660254037844386)
]

l_lignes = main()
infill = [element for sous_liste in l_lignes for element in sous_liste]

l_ratio = [i/1000 for i in range(1, 110, 10)][::2]

for ratio in tqdm(l_ratio):
    kernel = np.array(resize(kernel, ratio))
    
    """
    for i in range(10):
        infill.append([[i, j] for j in range(10)])
    """


    infill = np.array(infill)

    x, y = np.meshgrid(np.linspace(0.1, 0.9, 50), np.linspace(0.1, 0.9, 50))
    vectorized_density = np.vectorize(lambda x,y :density(x, y, kernel, infill))

    # Appliquer la fonction density sur la grille (x, y)
    z = vectorized_density(x, y)

    fig_3d = go.Figure()

    # Ajouter la surface 3D
    fig_3d.add_trace(go.Surface(z=z, x=x, y=y, colorscale="Viridis", name="Surface de f_s"))
    #fig_3d.add_trace(go.Scatter3d(z=z, x=x, y=y, mode='markers'))

    # Ajouter les courbes polygonales à la 3D, en fixant leur position z à 0



    for line in infill:
        fig_3d.add_trace(go.Scatter3d(x=line[:, 0], y=line[:, 1], z=np.zeros(len(line)), mode='lines'))

    # Ajouter le kernel à la 3D, en fixant également z à 0
    kernel_disp = np.append(kernel, [kernel[0]], axis=0)
    fig_3d.add_trace(go.Scatter3d(x=kernel_disp[:, 0], y=kernel_disp[:, 1], z=np.zeros(len(kernel_disp)), mode='lines'))

    # Mise à jour de la figure 3D
    fig_3d.update_layout(
        title="Densité",
        scene=dict(
            xaxis_title="x",
            yaxis_title="y",
            zaxis_title="D"
        ),
        width=1000,
        height=1000
    )

    # Afficher la figure 3D
    fig_3d.show()
