import pygame as py
import numpy as np


class SFI():
    def __init__(self, scale, rot, offset=np.array([[0], 
                                                    [0]])):
        self.A = np.array([[np.cos(rot), -np.sin(rot)], 
                            [np.sin(rot), np.cos(rot)]]) *  scale
        self.B = offset


    def compute_point(self, point):
        
        arr = np.array([[point[0]], [point[1]]])
        return tuple((self.A@arr + self.B).flatten())

    def compute_poly(self, poly):
        l_point_image = []
        for point in poly.l_points:
            l_point_image.append(self.compute_point(point))
        return Polyline(l_point_image)

class Polyline:
    def __init__(self, points=[], sfi=[]):
        self.l_points = []

        for (x, y) in points:
            self.add_point(x, y)

    
        self.l_subdiviser = []

    def pretty_print(self):
        print("Polyline avec", len(self.l_points), "points:")
        for i, point in enumerate(self.l_points):
            (x, y) = point # Assurez-vous que le point est un tableau 1D
            print(f"Point {i+1}: (x={x:.2f}, y={y:.2f})")


    def add_point(self, x, y, index=-1):
        self.l_points.insert(index, (x, y))

    def get_points(self):
        return self.l_points

    def _point_line_distance(self, point, start, end):
        """
        Calcule la distance perpendiculaire d'un point à une ligne définie par deux points.
        """
        px, py = point
        x1, y1 = start
        x2, y2 = end

        if x1 == x2 and y1 == y2:  # Le segment est un point
            return math.sqrt((px - x1) ** 2 + (py - y1) ** 2)

        # Projection du point sur le segment
        dx, dy = x2 - x1, y2 - y1
        t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t))  # Clamp t à [0, 1]
        proj_x, proj_y = x1 + t * dx, y1 + t * dy

        return math.sqrt((px - proj_x) ** 2 + (py - proj_y) ** 2)



    def subdivide(self, min_distance):
        """
        Subdivise les segments de la polyline en fonction d'une distance minimale.
        :param min_distance: La distance minimale entre deux points consécutifs.
        """
        if len(self.points) < 2 or min_distance <= 0:
            return  # Pas de subdivision nécessaire ou distance invalide

        new_points = [self.points[0]]  # Conserve le premier point
        for i in range(1, len(self.points)):
            x1, y1 = self.points[i - 1]
            x2, y2 = self.points[i]
            # Calcul de la distance entre les deux points
            segment_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            # Ajoute des points intermédiaires si nécessaire
            if segment_length > min_distance:
                num_divisions = math.ceil(segment_length / min_distance)
                for j in range(1, num_divisions):
                    t = j / num_divisions
                    x = (1 - t) * x1 + t * x2
                    y = (1 - t) * y1 + t * x2
                    new_points.append((x, y))
            new_points.append((x2, y2))  # Ajoute le point final du segment

        self.l_subdiviser = new_points

    def simplify(self, tolerance):
        """
        Simplifie la polyline en utilisant l'algorithme Ramer-Douglas-Peucker.
        :param tolerance: La distance maximale autorisée entre le point ignoré et la ligne simplifiée.
        """
        def rdp(points, tolerance):
            if len(points) < 3:
                return points  # Pas assez de points pour simplifier

            # Trouve le point le plus éloigné de la ligne formée par les extrémités
            start, end = points[0], points[-1]
            max_dist = 0
            index = 0

            for i in range(1, len(points) - 1):
                dist = self._point_line_distance(points[i], start, end)
                if dist > max_dist:
                    max_dist = dist
                    index = i

            # Si la distance maximale dépasse la tolérance, divise et simplifie récursivement
            if max_dist > tolerance:
                left = rdp(points[:index + 1], tolerance)
                right = rdp(points[index:], tolerance)
                return left[:-1] + right
            else:
                return [start, end]

        self.points = rdp(self.l_subdiviser, tolerance)
    



class Fractal():
    def __init__(self):
        self.l_SFI = [] # list of SFI function 
        self.l_iteration = [] #list of list of polyline (list (point)) (at each iteration)
        self.l_polyline = []

    def add_sfi(self,sfi):
        self.l_SFI.append(sfi)

    def add_polyline(self, poly):
        self.l_polyline.append(poly)
        self.l_iteration = [self.l_polyline]

    def compute_fractal(self, nb_iter=10, force=False):
        if force:
            self.l_iteration = [self.l_polyline]
        while len(self.l_iteration) < nb_iter:
            self.l_iteration.append([])
            print("--------------------------------------------------------------------")
            for SFI in self.l_SFI:    
                for poly in self.l_iteration[-2]:
                    #print(poly.l_points)
                    self.l_iteration[-1].append(SFI.compute_poly(poly))
    

class RenderFractal:
    def __init__(self, fractal):
        self.fractal = fractal
        self.screen = py.display.set_mode((1800, 1000))
        py.display.set_caption("Fractal Renderer")
        self.width, self.height = self.screen.get_size()
        self.screen.fill((0, 0, 0))

    def transform_point_to_screen(self, point):
        """Transforme un point en coordonnées écran."""
        x, y = point
        return (int(x), int(self.height-y))#int(self.width // 2 + x), int(self.height // 2 - y)

    def draw_polyline(self, polyline, color=(255, 255, 255)):
        """Dessine une polyline sur l'écran."""
        points = [self.transform_point_to_screen(p) for p in polyline.l_points]
        if len(points) > 1:
            py.draw.lines(self.screen, color, False, points, 1)

    def render(self):
        """Affiche le fractal."""
        self.screen.fill((0, 0, 0))
        for iteration in self.fractal.l_iteration:
            for polyline in iteration:
                self.draw_polyline(polyline)
        py.display.flip()


def koch_fractal():

    koch = Fractal()
    koch.add_polyline(Polyline([(0, 0), (1800, 0)]))
    #fractaladd_polyline(Polyline([(0, 1000), (1800, 1000)])).add_polyline(Polyline([(0, 1000), (1800, 1000)]))

    # Ajout de transformations (SFIs)
    sfi1 = SFI(scale=1/3, rot=0, offset=np.array([[0], [0]]))
    sfi2 = SFI(scale=1/3, rot=np.pi/3, offset=1800*np.array([[1/3], [0]]))
    sfi3 = SFI(scale=1/3, rot=-np.pi / 3, offset=1800*np.array([[1/2], [np.sqrt(3)/6]]))
    sfi4 = SFI(scale=1/3, rot=0, offset=1800*np.array([[2/3], [0]]))

    #sfi2 = SFI(scale=0.5, rot=np.pi / 3, offset=np.array([[50], [50]]))
    koch.add_sfi(sfi1)
    koch.add_sfi(sfi2)
    koch.add_sfi(sfi3)
    koch.add_sfi(sfi4)

    # Calcul du fractal
    koch.compute_fractal(nb_iter=8, force=True)
    return koch

def hilbert_fractal():
    hilbert = Fractal()

    hilbert.add_polyline(Polyline([(0, 0), (1800, 0)]))  # Ligne initiale

    # Ajout des transformations
    hilbert.add_sfi(SFI(scale=0.5, rot=-np.pi/2, offset=1800*np.array([[0], [0]])))
    hilbert.add_sfi(SFI(scale=0.5, rot=0, offset=1800*np.array([[0.5], [0]])))
    hilbert.add_sfi(SFI(scale=0.5, rot=0, offset=1800*np.array([[0.5], [0.5]])))
    hilbert.add_sfi(SFI(scale=0.5, rot=np.pi/2, offset=1800*np.array([[0], [0.5]])))

    hilbert.compute_fractal(nb_iter=10, force=1)
    return hilbert

# Exemple d'utilisation
if __name__ == "__main__":
    py.init()

    # Initialisation des polylines et transformations
    
    # Rendu
    renderer = RenderFractal(hilbert_fractal())
    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False

        renderer.render()

    py.quit()
