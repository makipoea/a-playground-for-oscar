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
                theta= np.pi*0.5
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
    lenght=(square[1][0]-square[0][0])*0.5
    if -np.pi*0.25<theta<np.pi*0.25 or np.pi*0.75<theta<np.pi*1.25:
        d_to_square= lenght/np.cos(theta)
    else:
        d_to_square=lenght/np.sin(theta) 
    return (abs(r/d_to_square))

#pour une liste donnée renvoie le ratio avec le point du carré de meme angle (avec le centre) pour chaque point ainsi que l'angle
def ratio_from_l_point(L_point,square):
    L_polar=polar_cordonates(L_point,square)
    
    l_ratio_angle=[]
    for polar_point in L_polar :
        rat=ratio(polar_point,square)
        theta=polar_point[1]
        l_ratio_angle.append((rat,theta))
    return l_ratio_angle

#genere une grille avec resolution point par ligne (tu peux faire de la 4K stv)
def grid(square,resolution):
    grille=[]
    dim= np.linspace(0,square[1][0]-square[0][0],num=resolution)
    for i in dim:
        for j in dim:
            grille.append((square[0][0]+i,square[0][1]+j))
    
    return grille

#genere l'image d'une grille de resolution donnée par la transformation carré-forme induite par la liste (j'ai pas vérifié la correction)        
def image(L_point,resolution):
    carré= square(L_point)          #Création du carré englobant la figure
    grille= grid(carré,resolution)  #Création de la grille dans ce meme carré
    func=sorted(ratio_from_l_point(L_point,carré),key= lambda point:point[1]) #Réalisation de la fonction associant le ratio en fonction de l'angle
    image=[]
    polar_grille=polar_cordonates(grille,carré) #Passage de la grille en coordonées polaire, pour utiliser la fonction
    for point in polar_grille: #On itère sur chaque point
        ind=0
        while ind<len(func) and point[1]>func[ind][1]: #recherche du point de la figure avec l'angle le plus proche
            ind+=1
        
        if ind==0 or ind==len(func):
            theta0=func[-1][1]
            theta1=func[0][1]+2*np.pi
            theta=point[1]
            if theta>0:   
                t=(theta-theta0)/(theta1-theta0)
            else:
                t=(theta+2*np.pi-theta0)/(theta1-theta0)
            rayon= point[0]*(func[-1][0]*(1-t)+func[0][0]*t)

        else:
            theta0=func[ind-1][1]
            theta1=func[ind][1]
            theta=point[1]
            t=(theta-theta0)/(theta1-theta0)
            rayon= point[0]*(func[ind-1][0]*(1-t)+func[ind][0]*t)  #Application du ratio sur le rayon en pondérant en fonction de la difference d'angle avec les points adjacents
        
        image.append((rayon,theta)) 
    return image
        
if __name__ == "__main__":
    
    import matplotlib.pyplot as plt

    #un exemple avec un octogone 100% handmade (il marche a peu prés à voir avec plus de points)
    L=[(1,0),(0.707,0.707),(0,1),(-0.707,0.707),(-1,0),(-0.707,-0.707),(0,-1),(0.707,-0.707)]

    carré= square(L)
    im=image(L,10)
    grille= grid(carré,10)
    L_polar= polar_cordonates(L,carré)
    fig,ax = plt.subplot_mosaic("AB",per_subplot_kw={"A":{"projection":"polar"}})

    ax["B"].plot([p[0] for p in L], [p[1] for p in L],marker='o',linestyle='') #Avant la transformation
    ax["B"].plot([p[0] for p in grille], [p[1] for p in grille],marker='*',linestyle='')
    Lp=polar_cordonates(L,carré)
    ax["A"].plot([p[1] for p in im],[p[0] for p in im],marker='*',linestyle='') #Aprés la transformation
    ax["A"].plot([p[1] for p in L_polar],[p[0] for p in L_polar],marker='o',linestyle='')
    plt.show()