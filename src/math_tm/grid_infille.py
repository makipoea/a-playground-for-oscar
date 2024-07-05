import numpy as np
import numpy.polynomial as npl 
import matplotlib.pyplot as plt 
from shapely.geometry import LineString, Point, Polygon
from mpl_toolkits.mplot3d import Axes3D

from regression import decompose, approx

def abscisse_line(start, end, polynome, theta ,nb_line):
    """
    a partir d'un polynome calcule par intergration les abscysse des lignes entre start et end (qui l'eu crut)
    """
    polynome = npl.Polynomial(polynome)
    print("polynome = ", polynome)

    primitive = polynome.integ()
    #print("primitive", primitive)

    l_image = np.linspace(primitive(start), primitive(end), nb_line).tolist()
    #del l_image[0]
    #del l_image[-1]
    #print(l_image)
    l_x = []
    l_droite = []

    c = np.cos(theta)
    s = np.sin(theta)

    for z in l_image:
        racine = [r.real for r in (primitive-npl.Polynomial(z)).roots() if r.imag == 0]
        for r in racine:
            if r>=start and end>=end:
                l_x.append(float(r))
                l_droite.append([(c*r, s*r), (r*c-s, s*r+c)])
                break

    return l_droite

def extend_line(droite, f=1000):
    p1 = np.array(droite[0])
    p2 = np.array(droite[1])

    vecteur = (p2-p1)/np.linalg.norm(p2-p1)
    return [p1-vecteur*f, p2+vecteur*f]

def generate_line_from_density(density_point, nb_polynome, degree, polygone, nb_line):
    parametre_finaux, angle, l_coeff = decompose(density_point, nb_polynome, degree)
    #print("angle =", angle)
    #for coeff in l_coeff:
    #    print(npl.Polynomial(coeff))
    infill_line = []

    x_density = np.array([point[0] for point in density_point])
    y_density = np.array([point[1] for point in density_point])

    r = np.sqrt(x_density**2+y_density**2)
    angle = np.arctan2( y_density, x_density)

    z_image = np.zeros(len(x_density))


    for theta, polynome in zip(angle, l_coeff):
        projection_polygone_on_line = []
        
        P = npl.Polynomial(polynome)
        #plot_polynome(x_density, y_density, P, theta)
        z = np.array(list(map(lambda r_,a : P(r_*np.cos(theta-a)), r, angle)))
        ax.scatter(x_density, y_density, z, c=np.random.uniform(0, 1, size=3), marker='x', s=100)
        print(z[0])
        z_image += z


        for (x, y) in polygone:
            theta_2 = theta-np.arctan(y/x)
            projection_polygone_on_line.append(np.sqrt(x**2+y**2)*np.cos(theta_2))
        
        start = min(projection_polygone_on_line)
        end = max(projection_polygone_on_line)
        l_droite = abscisse_line(start, end, polynome, theta, nb_line)
        for droite in l_droite:
            droite = LineString(extend_line(droite))
            #plt.plot([droite.coords[0][0], droite.coords[1][0]], [droite.coords[0][1], droite.coords[1][1]],[0, 0] , color="b")
            l_intersection = list(droite.intersection(Polygon(polygone)).coords)
       
            l_intersection = [point for point in l_intersection if point not in polygone]
            while l_intersection != []:
                infill_line.append([l_intersection[0], l_intersection[1]])
                del l_intersection[0]
                del l_intersection[0]
    

    print(z_image)
    ax.scatter(x_density, y_density, z_image, c=(0, 0, 0))

    return infill_line



def contraintes(x, y):
    return 3*x*y
    #return (x-0.5)*(y-0.5)+10
    #return (x-0.5)**2*y + 3*x*y

def boundingbox(points):
    """
    (min_x, min_y, max_x, max_y).
    """
    
    min_x = min(points, key=lambda point: point[0])[0]
    min_y = min(points, key=lambda point: point[1])[1]
    max_x = max(points, key=lambda point: point[0])[0]
    max_y = max(points, key=lambda point: point[1])[1]
    
    return (min_x, min_y, max_x, max_y)


def plot_polynome(x, y, polynome, theta):
    r = np.sqrt(x**2+y**2)
    angle = np.arctan2( y, x)
    z = np.array(list(map(lambda r,a : polynome(r*np.cos(theta-a)), r, angle)))
    ax.scatter(x, y, z, c=np.random.uniform(0, 1, size=3), marker='x', s=100)

if __name__ == "__main__":
    #polygone = [(2, 2), (2, 5), (10, 4), (9, 0), (6,1), (5, -1), (4, 3)]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #polygone = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    polygone = [(1, 1), (2, 1), (2, 2), (1, 2)]

    nb_contraintes = 10

    (min_x, min_y, max_x, max_y) = boundingbox(polygone)

    x = [] 
    y = [] 
    z = []

    for i in range(nb_contraintes+1):
        for j in range(nb_contraintes+1):
            x.append((max_x-min_x)/nb_contraintes*i+min_x)
            y.append((max_y-min_y)/nb_contraintes*j+min_y)

    x = np.array(x)
    y = np.array(y)
    z = np.array(list(map(contraintes, x, y)))
    #print(z)

    ax.scatter(x, y, z, color="r")

    infill = generate_line_from_density(list(zip(x, y, z)), 2, 2, polygone, 50)
    #print("infill = ", infill)

    last_point = polygone[0]
    for point in polygone[1::]:
        plt.plot([last_point[0], point[0]], [last_point[1], point[1]], [0, 0],color="g")
        last_point = point
    plt.plot([point[0], polygone[0][0]], [point[1], polygone[0][1]], [0, 0], color="g")

    for droite in infill:
        plt.plot([droite[0][0], droite[1][0]], [droite[0][1], droite[1][1]], [0, 0],color="b")

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    #ax.legend()

    plt.show()

