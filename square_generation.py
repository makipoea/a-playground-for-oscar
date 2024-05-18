import numpy as np

#crée le reste des points pour faire un polygone, les points etant donnés dans l'ordre !!!
def draw(L_point,number,close):
    result=[]
    distances=[0]*len(L_point)
    droites=[]
    sum=0
    for i in range(len(L_point)):
        if i==len(L_point)-1: 
            j = 0
        else : 
            j= i+1
        distances[i]=((L_point[i][0]-L_point[j][0])**2+(L_point[i][1]-L_point[j][1])**2)**0.5
        sum+=distances[i]
        droites.append(lambda x: ((L_point[i][1]-L_point[j][1])/(L_point[i][0]-L_point[j][0]))*(x-L_point[i][0])+L_point[i][1])
    
    if close : 
        iteration=range(len(L_point))
    else: 
        iteration=range(len(L_point)-1)
        sum-=distances[-1]
    for i in iteration :
        
        if i==len(L_point)-1: 
            j = 0
        else : 
            j= i+1
        abscisse=np.linspace(L_point[i][0],L_point[j][0],num=int(number*distances[i]/sum))
        
        for x in abscisse:
            result.append((x,droites[i](x)))
    
    return result
    



    
#génère un carre englobant tous les points de la figure
def square(L_point):
    xmin = min(L_point, key=lambda point:point[0])[0]
    xmax = max(L_point, key=lambda point:point[0])[0]
    ymin = min(L_point, key=lambda point:point[1])[1]
    ymax = max(L_point, key=lambda point:point[1])[1]
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

#En définissant l'origine au centre du carre passe les points en coordonnées polaires (theta varie de -pi/2 à 3pi/2 )
def from_cartesian_to_polar(L_point,square):
    # TO DO : simplify this function  
    center=square[4]
    L_polar=[(0, 0)]*len(L_point)
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


#Transformation inverse
def from_polar_to_cartesian(L_point,carre):
    center=carre[4]
    L_cart=[]
    for y in L_point:
        L_cart.append((y[0]*np.cos(y[1])+center[0],y[0]*np.sin(y[1])+center[1]))
    return L_cart

#donne le ratio du rayon entre un point en coordonnées polaire et le point du carre associé (theta identique)
def ratio(polar_point,square):
    r,theta=polar_point[0],polar_point[1]
    lenght=(square[1][0]-square[0][0])*0.5
    if -np.pi*0.25<theta<np.pi*0.25 or np.pi*0.75<theta<np.pi*1.25:
        d_to_square= lenght/np.cos(theta)
    else:
        d_to_square=lenght/np.sin(theta) 
    return (abs(r/d_to_square))

#pour une liste donnée renvoie le ratio avec le point du carre de meme angle (avec le centre) pour chaque point ainsi que l'angle
def ratio_from_l_point(L_point,square):
    L_polar=from_cartesian_to_polar(L_point,square)
    
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

#genere l'image d'un point du polygone dans le carre
def pol_to_square(Polygon,carre,point):
    center=carre[4]
    func=sorted(ratio_from_l_point(Polygon,carre),key= lambda point:point[1]) #Réalisation de la fonction associant le ratio en fonction de l'angle
    image=[]
    polar_point=from_cartesian_to_polar([point],carre)[0] #Passage de la grille en coordonées polaire, pour utiliser la fonction
    ind=0
    while ind<len(func) and polar_point[1]>func[ind][1]: #recherche du point de la figure avec l'angle le plus proche
        ind+=1
        
    if ind==0 or ind==len(func):
        theta0=func[-1][1]
        theta1=func[0][1]+2*np.pi
        theta=polar_point[1]
        if theta>0:   
            t=(theta-theta0)/(theta1-theta0)
        else:
            t=(theta+2*np.pi-theta0)/(theta1-theta0)
        rayon= polar_point[0]*((1/func[-1][0])*(1-t)+(1/func[0][0])*t)

    else:
        theta0=func[ind-1][1]
        theta1=func[ind][1]
        theta=polar_point[1]
        t=(theta-theta0)/(theta1-theta0)
        rayon= polar_point[0]*((1/func[ind-1][0])*(1-t)+(1/func[ind][0])*t)  #Application du ratio inverse sur le rayon en pondérant en fonction de la difference d'angle avec les points adjacents
        
    
    image=(rayon*np.cos(theta)+center[0],rayon*np.sin(theta)+center[1])
    
    return image


#genere l'image d'un point du carre dans le polygone associé (carre et polygone prédefinis)        
def square_to_pol(Polygon,carre,point):       
    func=sorted(ratio_from_l_point(Polygon,carre),key= lambda point:point[1]) #Réalisation de la fonction associant le ratio en fonction de l'angle
    image=[]
    polar_point=from_cartesian_to_polar([point],carre)[0] #Passage de la grille en coordonées polaire, pour utiliser la fonction
    ind=0
    while ind<len(func) and polar_point[1]>func[ind][1]: #recherche du point de la figure avec l'angle le plus proche
        ind+=1
        
    if ind==0 or ind==len(func):
        theta0=func[-1][1]
        theta1=func[0][1]+2*np.pi
        theta=polar_point[1]
        if theta>0:   
            t=(theta-theta0)/(theta1-theta0)
        else:
            t=(theta+2*np.pi-theta0)/(theta1-theta0)
        rayon= polar_point[0]*(func[-1][0]*(1-t)+func[0][0]*t)

    else:
        theta0=func[ind-1][1]
        theta1=func[ind][1]
        theta=polar_point[1]
        t=(theta-theta0)/(theta1-theta0)
        rayon= polar_point[0]*(func[ind-1][0]*(1-t)+func[ind][0]*t)  #Application du ratio sur le rayon en pondérant en fonction de la difference d'angle avec les points adjacents
        
    image=(rayon,theta) 
    return image

#a partir de deux points du polygone dessine la courbe entre les deux.
def draw_the_curve(L_point_polygon,L_point_curve,number):
    carre=square(L_point_polygon) 
    Polygon=draw(L_point_polygon,number,True) 
    L_point_curve_in_square=[]
    for point in L_point_curve:
        L_point_curve_in_square.append(pol_to_square(Polygon,carre,point)) #projection des points a relier dans le repére du carre
    
    L_point_to_draw=draw(L_point_curve_in_square,number,False) #relie les points avec des droites
    L_point_drawn=[]
    for point in L_point_to_draw:
        L_point_drawn.append(square_to_pol(Polygon,carre,point)) #projection dans le repère du polygone
    
    return L_point_drawn

def image_point(L_point_polygon, L):
    carre = square(L)
    L_point

if __name__ == "__main__":
    
    import matplotlib.pyplot as plt

    #un exemple avec un octogone 100% handmade (il marche a peu prés à voir avec plus de points)
    L=[(1,0),(0.707,0.707),(0,1),(-0.707,0.707),(-1,0),(-0.707,-0.707),(0,-1),(0.707,-0.707)]
    K=[(-0.25,3**0.5/4),(-0.25,-3**0.5/4),(0.5,0)]
    #L = [[396, 248], [486, 148], [634, 138], [695, 230], [651, 344], [482, 340]]
    #K = [[461, 216], [611, 153]]
    resultat=draw_the_curve(L,K,5)
    print(resultat)
    fig,ax=plt.subplot_mosaic("AB",per_subplot_kw={"A":{"projection":"polar"}})
    ax["A"].plot([p[1] for p in resultat],[p[0] for p in resultat],marker='x',linestyle='')
    Pol=draw(L,20,True)
    carre=square(L)
    Polnord=from_cartesian_to_polar(Pol,carre)
    ax["A"].plot([p[1] for p in Polnord],[p[0] for p in Polnord],marker='o',linestyle='dotted')
    ax["B"].plot([p[0] for p in Pol],[p[1] for p in Pol],marker='o',linestyle='dotted')
    ax["B"].plot([p[0] for p in K],[p[1] for p in K],marker='x',linestyle='')
    plt.show()
    
    '''Pol=draw(L,200,True)
    carre= square(L)
    grille= grid(carre,10)
    im=[]
    for x in grille:
        im.append(square_to_pol(Pol,carre,x))

    L_polar= from_cartesian_to_polar(L,carre)
    fig,ax = plt.subplot_mosaic("AB",per_subplot_kw={"A":{"projection":"polar"}})

    ax["B"].plot([p[0] for p in Pol], [p[1] for p in Pol],marker='o',linestyle='') #Avant la transformation
    ax["B"].plot([p[0] for p in grille], [p[1] for p in grille],marker='*',linestyle='')
    Lp=from_cartesian_to_polar(L,carre)
    ax["A"].plot([p[1] for p in im],[p[0] for p in im],marker='*',linestyle='') #Aprés la transformation
    ax["A"].plot([p[1] for p in L_polar],[p[0] for p in L_polar],marker='o',linestyle='')
    plt.show()'''

    '''L=[(1,0),(0.707,0.707),(0,1),(-0.707,0.707),(-1,0),(-0.707,-0.707),(0,-1),(0.707,-0.707)]
    Pol=polygonise(L,200,True)
    ax= plt.subplot()
    ax.plot([p[0] for p in Pol],[p[1] for p in Pol],marker='x',linestyle='')
    plt.show()'''
