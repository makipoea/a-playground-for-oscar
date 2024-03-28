import matplotlib as mp
import numpy as np

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
    return (c1,c2,(xmin,ydeb),(xmax,yfin))

def sort_with_x(L):
    G=[L[0]]
    for i in range(1,len(L)):
        j=0
        while j<len(G) and L[i][0]>=G[j][0]:
            j+=1
        G=G[0:j]+[L[i]]+G[j::]
    return G

def foo()