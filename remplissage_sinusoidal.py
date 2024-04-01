import matplotlib.pyplot as plt
import numpy as np


def slice_polygon(L_point):
    """
    L_point : point = (x, y)
    Coupe le polygone sur une diagonale(xmin a xmax)
    """
    xmin,xmax = L_point[0][0],L_point[0][0]
    ydeb, yfin = L_point[0][1],L_point[0][1]
    for point in L_point:
        if point[0]< xmin :
            xmin = point[0]
            ydeb= point[1]
        if point[0]>xmax :
            xmax = point[0]
            yfin= point[1]

    c1=[]
    c2=[]
    
    for point in L_point:
        (x,y) = point
        t = (xmax-x)/(xmax-xmin)
        if y <= ydeb*t + (1-t)*yfin :
            c2.append((x,y))
        else :
            c1.append((x,y))
    
    c1.append((xmin,ydeb))
    c1.append((xmax,yfin))

    return (c1,c2)


def sort_with_x(L_point):
    '''Trie une liste de couple par la valeur de chaque premier element de chaque couple'''
    
    L_trier = [L_point[0]]
    for i in range(1,len(L_point)):
        j=0
        while j<len(L_trier) and L_point[i][0]>=L_trier[j][0]:
            j+=1
        L_trier=L_trier[0:j]+[L_point[i]]+L_trier[j::]
    return L_trier

# je sais que c'est moins styler et pedagogique mais tu peux faire : sorted(L_points, key=lambda point: point[0])
# en gros lambda point: point[0] est une fonction (qui renvoie x) et qu'il vas appliquer a chaque element de la liste et 
# au lieu de trier la liste sur ses elements il trie la liste sur les outputs

def polygonfunc(L_point,L_abscisse):
    
    """A partir d'une liste de points d'abscisses (X1<X2<..<Xn) définie la fonction qui a x 
    renvoie son ordonnée sur la ligne brisée[(x1,y1)...(xn,yn)]"""
    L_ordonees=[]
    for x in L_abscisse :
        
        for i in range(len(L_point)-1):
            if x>= L_point[i][0] and x<=L_point[i+1][0] :
                t= (L_point[i+1][0]-x)/(L_point[i+1][0]-L_point[i][0])
                y = L_point[i][1]*t + (1-t)*L_point[i+1][1]
        L_ordonees.append(y)
    return L_ordonees


def fillpolygon(L,nbperiod):
    """A partir d'une liste de points définissant un polygone convexe, renvoie le remplissage associé (la fonction fill)"""
    (a,b) = slice_polygon(L)
    
    L1=sort_with_x(a)
    L2=sort_with_x(b)
    Lx=np.linspace(L1[0][0],L1[-1][0],(L1[-1][0]-L1[0][0])*nbperiod*10)
    f1= polygonfunc(L1,Lx)
    f2= polygonfunc(L2,Lx)
    fill=[0 for i in range(len(Lx))]
    pulsation = 2*np.pi*nbperiod/(L1[-1][0]-L1[0][0])
    
    for x in range(len(Lx)):
        fill[x]=0.5*(f1[x]-f2[x])*np.sin(Lx[x]*pulsation)+(f1[x]+f2[x])*0.5
    return Lx,fill

if __name__ == "__main__":
    #un exemple avec un hexagone avec 10 périodes de sinusoides
    fig, ax = plt.subplots()
    K=[(0,0),(1,1),(2,1),(3,0),(1,-1),(2,-1)]

    (Li,f) = fillpolygon(K,10)
    ax.plot(Li,f)
    L=slice_polygon([(0,0),(1,1),(2,1),(3,0),(1,-1),(2,-1)])

    a=sort_with_x(L[0])
    b=sort_with_x(L[1])
    print(a,b)

    Lx=np.linspace(0,3,100)

    ax.plot(Lx, polygonfunc(a,Lx))
    ax.plot(Lx, polygonfunc(b,Lx))


    plt.show()
