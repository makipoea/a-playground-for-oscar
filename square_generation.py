import matplotlib.pyplot as plt
import numpy as np

#génère un carré englobant tous les points de la figure
def square(L_point):
    L_trie= sorted(L_point, key=lambda point:point[0])
    xmin,xmax = L_trie[0][0],L_trie[-1][0]
    L_trie= sorted(L_point, key=lambda point:point[1])
    ymin,ymax= L_trie[0][1],L_trie[-1][1]
    lx= xmax-xmin
    ly= ymax-ymin
    if lx>=ly :
        yinf=ymin-(lx-ly)*0.5
        ysup=ymax+(lx-ly)*0.5
        xinf,xsup=xmin,xmax
    else :
        xinf=xmin-(ly-lx)*0.5
        xsup=xmax+(ly-lx)*0.5
        yinf,ysup=ymin,ymax


    return [(xinf,yinf),(xsup,yinf),(xsup,ysup),(xinf,ysup),((xinf+xsup)*0.5,(yinf+ysup)*0.5)]

#En définissant l'origine au centre du carré passe les points en coordonnées polaires (theta varie de -pi/2 à 3pi/2 )
def polar_cordonates(L_point,square):
    center=square[4]
    L_polar=[(0,0) for i in range(len(L_point))]
    for i in range(len(L_point)) :
        if L_point[i][0]==center[0]:
            if L_point[i][1]>center[1]:
                theta= np.pi*0,5
            else :
                theta = -np.pi*0.5
            r = abs(center[1]-L_point[i][1])
        else :
            if L_point[i][0]>center[0]:
                theta = np.arctan((L_point[i][1]-center[1])/(L_point[i][0]-center[0]))
            else:
                theta = np.arctan((L_point[i][1]-center[1])/(L_point[i][0]-center[0]))+ np.pi
            r= ((L_point[i][0]-center[0])**2+(L_point[i][1]-center[1])**2)**0.5
        L_polar[i]=(r,theta)
    return L_polar

#donne le ratio du rayon entre un point en coordonnées polaire et le point du carré associé (theta identique)
def ratio(polar_point,square):
    r,theta=polar_point[0],polar_point[1]
    lenght=square[1][0]-square[0][0]
    if -np.pi*0.25<theta<np.pi*0.25 or np.pi*0.75<theta<np.pi*1.25:
        d_to_square= length/np.cos(theta)
    else:
        d_to_square=lenght/np.sin(theta)
    return (r/d_to_square)


#un exemple avec l'hexagone
L=[(0,0),(1,1),(2,1),(3,0),(1,-1),(2,-1)]
square=square(L)
fig,ax = plt.subplot_mosaic("AB",per_subplot_kw={"A":{"projection":"polar"}})
ax["B"].plot([p[0] for p in L], [p[1] for p in L],marker='*',linestyle='')
ax["B"].plot([p[0] for p in square], [p[1] for p in square],marker='o',linestyle='')
Lp=polar_cordonates(L,square)
ax["A"].plot([p[1] for p in Lp],[p[0] for p in Lp],marker='*',linestyle='')
plt.show()