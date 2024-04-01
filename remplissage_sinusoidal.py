import matplotlib.pyplot as plt
import numpy as np

#Coupe le polygone sur une diagonale(xmin a xmax)
def slice_polygon(L):
    xmin,xmax = L[0][0],L[0][0]
    ydeb, yfin = L[0][1],L[0][1]
    for u in L:
        if u[0]< xmin :
            xmin = u[0]
            ydeb= u[1]
        if u[0]>xmax :
            xmax = u[0]
            yfin= u[1]
    print ((xmin,ydeb),(xmax,yfin))

    c1=[]
    c2=[]
    
    for u in L:
        x,y= u[0],u[1]
        t = (xmax-x)/(xmax-xmin)
        if y <= ydeb*t + (1-t)*yfin :
            c2.append((x,y))
        else :
            c1.append((x,y))
    
    c1.append((xmin,ydeb))
    c1.append((xmax,yfin))

    return (c1,c2)

#Trie une liste de couple par la valeur de chaque premier element de chaque couple
def sort_with_x(L):
    G=[L[0]]
    for i in range(1,len(L)):
        j=0
        while j<len(G) and L[i][0]>=G[j][0]:
            j+=1
        G=G[0:j]+[L[i]]+G[j::]
    return G

#A partir d'une liste de points d'abscisses (X1<X2<..<Xn) définie la fonction qui a x renvoie son ordonnée sur la ligne brisée[(x1,y1)...(xn,yn)]
def polygonfunc(Points,abscisse):
    ordonees=[]
    for x in abscisse :
        
        for i in range(len(Points)-1):
            if x>= Points[i][0] and x<=Points[i+1][0] :
                t= (Points[i+1][0]-x)/(Points[i+1][0]-Points[i][0])
                y = Points[i][1]*t + (1-t)*Points[i+1][1]
        ordonees.append(y)
    return ordonees

#A partir d'une liste de points définissant un polygone convexe, renvoie le remplissage associé (la fonction fill)
def fillpolygon(L,nbperiod):
    (a,b) = slice_polygon(L)
    
    L1=sort_with_x(a)
    L2=sort_with_x(b)
    print(L1,L2)
    Lx=np.linspace(L1[0][0],L1[-1][0],(L1[-1][0]-L1[0][0])*nbperiod*10)
    print(Lx)
    f1= polygonfunc(L1,Lx)
    f2= polygonfunc(L2,Lx)
    fill=[0 for i in range(len(Lx))]
    pulsation = 2*np.pi*nbperiod/(L1[-1][0]-L1[0][0])
    
    for x in range(len(Lx)):
        fill[x]=0.5*(f1[x]-f2[x])*np.sin(Lx[x]*pulsation)+(f1[x]+f2[x])*0.5
    return Lx,fill

#un exemple avec un hexagone avec 10 périodes de sinusoides
fig, ax = plt.subplots()
K=[(0,0),(1,1),(2,1),(3,0),(1,-1),(2,-1)]

(Li,f) = fillpolygon(K,10)
ax.plot(Li,f)
L=slice_polygon([(0,0),(1,1),(2,1),(3,0),(1,-1),(2,-1)])
print(L)
a=sort_with_x(L[0])
b=sort_with_x(L[1])

Lx=np.linspace(0,3,100)

ax.plot(Lx, polygonfunc(a,Lx))
ax.plot(Lx, polygonfunc(b,Lx))




plt.show()