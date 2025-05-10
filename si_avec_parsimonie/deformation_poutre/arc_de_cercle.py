import matplotlib.pyplot as plt
#from  scimpy.abc import r , x
#from simpy import solve
from math import sin, pi, cos
import numpy as np
from scipy.optimize import fsolve

R1 = 1
theta1 = 1
l = 0.01
e = 1
K = 1000

def x_of(theta):
    return 2*sin(theta/2)

def vectoriel(theta, R):
    #print(theta, R)
    mat_trans = np.array([[2*sin(theta/2), R*cos(theta/2)], 
                        [2*R*theta**2-2*R1*theta*theta1, 2*R**2*theta-2*R*R1*theta1]])
    #print(mat_trans)
    return np.linalg.det(mat_trans)

def force(theta, R):
    return K*e*l*np.cos(theta/2)*(R*theta - R1*theta1)


if __name__ == "__main__":
    l_R = list(i/10 for i in range(10, 30))
    #l_R = [1.1]
    l_theta = []
    #print(vectoriel(10, 10))
    
    
    for R in l_R:
        theta = fsolve(lambda theta:vectoriel(theta[0], R), pi/2)[0]
        l_theta.append(theta)

    l_theta = np.array(l_theta)
    l_R = np.array(l_R)

    l_x = 2*l_R*np.sin(l_theta/2)
    l_force = force(l_theta, l_R)
    
    plt.plot(l_x, l_theta, color='red')
    plt.plot(l_x, l_R, color = 'green')
    #plt.plot(l_x, l_force, color='blue')
    plt.show()


    
