import cv2
import numpy as np 
import matplotlib.pyplot as plt
##############################################################
#INPUT
length_of_touillete = 150 # in mm
width_of_touillete = 20
#OUTPUT (size of the ouput image in pixels bigger = more presize)
size_x = 2000
##############################################################


def compute_contour(name_file, extrusion_thickness=0.5, epsilon=1):
    #white_background = np.ones((size_y,size_x , 3), dtype=np.uint8) * 255 
    
    img = cv2.imread(name_file)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    
    contours = contours[1:]
    l_point = np.vstack(contours)
    
    x, y, w, h = cv2.boundingRect(l_point)


    mm_over_image_pixel = length_of_touillete/w

    expension_ratio = size_x/(w+10*extrusion_thickness/mm_over_image_pixel)
 
    padding = 5*extrusion_thickness/mm_over_image_pixel
    translation_vector = -np.array([x, y])+np.array([padding, padding])
    
    contours = [np.int32((contour+translation_vector)*expension_ratio) for contour in contours]

    white_background = np.ones((int((h+2*padding)*expension_ratio),size_x , 3), dtype=np.uint8) * 255 

    cv2.drawContours(image=white_background, contours=contours, contourIdx=-1, color=(0, 0, 0), thickness=int(extrusion_thickness/mm_over_image_pixel*expension_ratio))

    # On a calculer l'extrusion, maintenant on l'exporte en svg

    img_gray = cv2.cvtColor(white_background, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
    contours_extrusion, _ = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    contours_extrusion = [contour/expension_ratio for contour in contours_extrusion[1:]]

    contours_extrusion = [contour.reshape(-1, 2).tolist() for contour in contours_extrusion]

    if epsilon:
        for i, contour, in enumerate(contours_extrusion):
            if len(contour) == 0:  # Vérifie si le contour est vide
                continue
            contours_extrusion[i] =  cv2.approxPolyDP(np.array(contour, dtype=np.float32), epsilon, True)
    
        contours_extrusion = [contour.reshape(-1, 2).tolist() for contour in contours_extrusion]

    return contours_extrusion

if __name__ == '__main__':
    contours_extrusion = compute_contour("eprouvette_1.png")
    
    for contour in contours_extrusion:  
        plt.scatter([p[0] for p in contour], [p[1] for p in contour], marker='x', s=1)

    plt.show()