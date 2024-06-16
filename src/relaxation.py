import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point, Polygon # oui j'ai eu la flemme 
from copy import deepcopy

def segment_intersect_polyline(s, polyline):
    s1 = LineString(s)
    last_point = polyline[0]
    for point in polyline[1::]:
        s2 = LineString([last_point, point])
        if s1.intersects(s2) and point not in s and last_point not in s:
            return 1
            last_point = point
    return 0

def self_intersect(polyline):
    for i in range(len(polyline) - 1):
        segment1 = LineString([polyline[i], polyline[i + 1]])
        for j in range(i + 2, len(polyline) - 1):
            segment2 = LineString([polyline[j], polyline[j + 1]])
            if segment1.intersects(segment2):
                return True
    return False

def polyline_intersects_polygon(polyline, polygon):

    polygon_shape = Polygon(polygon)

    for i in range(len(polyline) - 1):
        segment = LineString([polyline[i], polyline[i + 1]])

        if segment.intersects(polygon_shape):
            return True
    
    return False

def update(polygone, polyline, min_distance=None, alpha=0.1):
    """
    alpha must be between 0 and 1 
    """
    polygone = deepcopy(polygone)
    polyline = deepcopy(polyline)

    for i, update_point in enumerate(polyline):
        max_distance = 0
        max_point = -1 #update_point # point du polygone atteignable de distance maximale
        for point in polygone:
            if not segment_intersect_polyline([update_point, point], polygone+[polygone[0]]) and not segment_intersect_polyline([update_point, point], polyline):
                #print("OK", update_point)
                d = Point(update_point).distance(Point(point)) 
                if d > max_distance:
                    max_point = point
                    max_distance = d

        if max_point != -1:
            a = alpha
            new_point = [max_point[0] * a + update_point[0] * (1 - a), max_point[1] * a + update_point[1]*(1 - a)]
            new_polyline = polyline.copy()
            new_polyline[i] = new_point
            while self_intersect(new_polyline): #or not polyline_intersects_polygon(new_polyline, polygone):
                print("bloquer", a)
                a /= 2
                new_point = [max_point[0] * a + update_point[0] * (1 - a), max_point[1] * a + update_point[1] * (1 - a)]
                new_polyline[i] = new_point
            #if not self_intersect(new_polyline) and not LineString(new_polyline).intersects(Polygon(polygone)):
            polyline[i] = new_point
            #print("ok")
        
    return polyline

def supdivise(polyline, s=2):
    new_polyline = []

    for i in range(len(polyline) - 1):
        start_point = polyline[i]
        end_point = polyline[i + 1]

        # Add the start point of the segment
        new_polyline.append(start_point)

        # Compute the subdivisions
        for j in range(1, s):
            t = j / s
            subdiv_point = (
                start_point[0] * (1 - t) + end_point[0] * t,
                start_point[1] * (1 - t) + end_point[1] * t
            )
            new_polyline.append(subdiv_point)

    # Add the last point of the polyline
    new_polyline.append(polyline[-1])

    return new_polyline


def display_polygone(polygone, c='red'):
    last_point = polygone[0]
    for point in polygone[1::]+[last_point]: 
        plt.plot([last_point[0], point[0]], [last_point[1], point[1]], lw=0.5, color=c)
        last_point = point

def display_polyline(polyline, c='green'):
    last_point = polyline[0]
    for point in polyline[1::]:
        plt.plot([last_point[0], point[0]], [last_point[1], point[1]], lw=0.5, color=c)
        last_point = point


if __name__ == "__main__":
    #polygone = [(1,0),(0.71,0.71),(0,1),(-0.71, 0.71),(-1,0),(-0.71,-0.71),(0,-1),(0.71,-0.71)]
    polygone = [(2, 2), (2, 5), (10, 4), (9, 0), (6,1), (5, -1), (4, 3)]
    polyline = supdivise([(3, 4), (5, 3), (6, 2), (8, 1)], 20)
    #polyline = [(3, 4), (5, 3)]
    #new_polyline = update(polygone, polyline)
    #display_polyline(new_polyline, c="blue")
    #b = LineString(polyline).intersects(Polygon(polygone))
    #print(b)
    
    display_polygone(polygone)
    display_polyline(polyline)

    for i in range(10):
        polyline = update(polygone, polyline, alpha=0.1)
    display_polyline(polyline, c="blue")
    
    plt.show()
    