import cv2
import numpy as np 
import svgwrite
##############################################################
#INPUT
extrusion_thickness = 0.5 # in mm
length_of_touillete = 150 # in mm
width_of_touillete = 20
#OUTPUT (size of the ouput image in pixels)
size_x = 2000
##############################################################


def compute_file(name_file):
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

    dwg = svgwrite.Drawing('extrusion.svg', profile='tiny', size=(f'{length_of_touillete}mm', f'{width_of_touillete}mm'))

    for contour in contours_extrusion[1:]:
        points = [(point[0][0], point[0][1]) for point in contour]
        path = dwg.path(d="M" + " L".join(f"{x},{y}" for x, y in points) + " Z", fill='none', stroke='black')
        dwg.add(path)

    dwg.save()


    cv2.imwrite("extrusion.png", white_background)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("hello world!")

    compute_file("eprouvette_1.png")