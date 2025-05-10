import os 
import sys 
import importlib
import FreeCAD, FreeCADGui, Part, Draft
import Fem , FemGui
import ObjectsFem
from femmesh.gmshtools import GmshTools as gt
from femtools import ccxtools

import os
print(os.getcwd())
workdir="/home/makipoea/Documents/prepa/tipe/programme/a-playground-for-oscar/src/freecad_simulation"
os.chdir(workdir)
sys.path.append(workdir)
sys.path.append(workdir)
print(os.getcwd())
print(os.listdir())
print(sys.path)
import matplotlib.pyplot as plt

import generate_coutour

importlib.reload(generate_coutour)

from generate_coutour import compute_contour

################################################################################
#CREATION DU MODELE 3D# 
################################################################################
doc = FreeCAD.newDocument("simulation mécanique")

def create_3D_model(file_name, infill_height=20, bottom_height=0, top_height=0,  extrusion_thickness=0.5):
    """
    height : hauteur du remplissage de la touillette en mm
    extrusion_width : largeur de l'extrusion en mm (epaisseur du filament lors de l'extrusion )
    """
    doc = App.ActiveDocument
    contours_extrusion = compute_contour(file_name, extrusion_thickness)
    
    # Liste pour stocker les formes des contours
    wires = []
    for i, contour in enumerate(contours_extrusion):
        points = [FreeCAD.Vector(p[0], p[1], 0) for p in contour]
        
        if points[0] != points[-1]: # on ferme le contour si il n'est pas fermé 
            points.append(points[0])
    
        try:
            wire = Part.Wire(Part.makePolygon(points))
            wires.append(wire)
        except Exception as e:
            print(f"Erreur lors de la création du wire {i}: {e}")
    
    FreeCAD.ActiveDocument.recompute()
    
    #  Identifier le contour principal (le plus grand)
    wires.sort(key=lambda w: w.BoundBox.DiagonalLength, reverse=True)
    main_wire = wires[0]  # Plus grand contour = pièce principale
    holes = wires[1:]  # Tous les autres sont des trous
    
    # Construire la face avec les trous
    try:
        
        base_infill = Part.Face([main_wire] + holes)  # Fusionner le contour principal avec les trous
        eprouvette_solid = base_infill.extrude(FreeCAD.Vector(0, 0, infill_height))  # Extrusion
       
        if bottom_height:
            base_bottom = Part.Face([main_wire])
            bottom_solid = base_bottom.extrude(FreeCAD.Vector(0, 0, -bottom_height))
            eprouvette_solid = eprouvette_solid.fuse(bottom_solid)
        
        if top_height:
            base_top = Part.Face([main_wire])
            top_solid = base_top.extrude(FreeCAD.Vector(0, 0, top_height))
            top_solid.translate(FreeCAD.Vector(0, 0, infill_height))
            eprouvette_solid = eprouvette_solid.fuse(top_solid)
        
        final_part = doc.addObject("Part::Feature", "eprouvette")
        final_part.Shape = eprouvette_solid
    
        FreeCAD.ActiveDocument.recompute()
        return final_part
    except Exception as e:
        print(f"Erreur lors de la création de la face: {e}")


################################################################################
#SIMULATION NUMERIQUE# 
################################################################################

def add_simulation():
    """
    add parameter for density oyung module etc 
    """
    FreeCADGui.activateWorkbench("FemWorkbench")
    
    # Active l'analyse 
    analysis = ObjectsFem.makeAnalysis(FreeCAD.ActiveDocument, 'Analysis')
    FemGui.setActiveAnalysis(analysis)
    
    #solver = ObjectsFem.makeSolverCalculixCcxTools(doc)
    #analysis.addObject(solver)
    

    material = ObjectsFem.makeMaterialSolid(FreeCAD.ActiveDocument, "Material")
    
    
    material.Material = {
        'Name': 'Pla ou quoi ? ',
        'Density': '1250 kg/m^3',
        'YoungsModulus': '3640 MPa',
        'PoissonRatio': '0.36'
    }
    
    
    """
    material.Material = {
        'Name': 'PLA-Generic',
        'Density': '1240 kg/m^3',
        'YoungsModulus': '3640 MPa',
        'PoissonRatio': '0.36'
    }
    """
    
    analysis.addObject(material)
    
    FreeCAD.ActiveDocument.recompute()
    return analysis
    # ajouter une face fixe 

def add_constraints(piece, analysis, force):
    
    # Initialiser les variables pour les faces avec x_min et x_max
    d_center_of_mass = {i:face.CenterOfMass.x for i, face in enumerate(piece.Shape.Faces)}

    x_min = min(d_center_of_mass.values())
    x_max = max(d_center_of_mass.values())
    
    index_x_min = [index for index, x in d_center_of_mass.items() if x == x_min]
    index_x_max = [index for index, x in d_center_of_mass.items() if x == x_max]
    
    # Vérifier que les faces ont été trouvées
    if not index_x_min or not index_x_max:
        raise ValueError("Les faces avec x_min et x_max n'ont pas été trouvées.")
   
    # Pour une raison que je ne preciserait pas nos cher amis les developeurs se sont dit que le
    # meilleur moyen de donner une DIRECTION c'est de donner un arrete par ce que je cite 
    # <<les vecteurs{}c'est{}pas{}fun>>
    
    line = Part.LineSegment(App.Vector(0, 0, 0), App.Vector(1, 0, 0))
    useful_line = App.ActiveDocument.addObject("Part::Feature", "DirectionEdge")
    useful_line.Shape = line.toShape()
    useful_line.Visibility = False # Juste pour le Quart d'heure perdu
    
    # Ajouter la contrainte fixe à la face avec x_min
    constraint_fixed = App.ActiveDocument.addObject("Fem::ConstraintFixed", "ConstraintFixed")
    constraint_fixed.References = [(piece, f"Face{i + 1}") for i in index_x_min]
    constraint_fixed.Scale = 1  # Ajustez l'échelle si nécessaire
    analysis.addObject(constraint_fixed)
    
    # Ajouter la contrainte de force à la face avec x_max
    constraint_force = App.ActiveDocument.addObject("Fem::ConstraintForce", "ConstraintForce")
    constraint_force.Force = force * 1000  # Valeur de la force en milli Newtons
    constraint_force.Direction = (useful_line, "Edge1")
    constraint_force.Reversed = False
    constraint_force.Scale = 1
    constraint_force.References = [(piece, f"Face{i + 1}") for i in index_x_max]

    analysis.addObject(constraint_force)
   
    App.ActiveDocument.recompute()
    
    return constraint_force


# Creation du maillage 

def compute_maillage(piece):
    femmesh_obj = ObjectsFem.makeMeshGmsh(doc, "FinalPiece_Mesh")
    femmesh_obj.Shape = piece#doc.piece_name  # Associer la géométrie
    
    femmesh_obj.ElementOrder = '2nd'  # '1st' pour premier ordre, '2nd' pour second ordre
    femmesh_obj.SecondOrderLinear = False

    doc.recompute()

    gmsh_mesh = gt(femmesh_obj)
    error = gmsh_mesh.create_mesh()  # Exécuter Gmsh

    if error:
        print(f"Erreur lors du maillage Gmsh : {error}")

# Ajouter le maillage à l'analyse FEM active
#FemGui.getActiveAnalysis().addObject(femmesh_obj)
    analysis.addObject(femmesh_obj)


def add_solveur():
    # On lance la simulation   
    solver = ObjectsFem.makeSolverCalculiXCcxTools(doc)
    solver.AnalysisType = 0
    solver.EigenmodesCount = 10
    solver.EigenmodeLowLimit = 0.0
    solver.EigenmodeHighLimit = 1000000.0   # Pour tous ceux qui se demande, j'ai bien entendu ecris toutes ces valeurs à la main 
    solver.IterationsMaximum = 2000         # si pour vous elles ne sont pas evidentes skills issue
    solver.TimeInitialStep = 1.0
    solver.TimeEnd = 1.0
    solver.TimeMinimumStep = 1e-05
    solver.TimeMaximumStep = 1.0
    solver.ThermoMechSteadyState = True
    solver.IterationsControlParameterTimeUse = False
    solver.SplitInputWriter = False
    solver.MatrixSolverType = 0
    solver.BeamShellResultOutput3D = True
    solver.GeometricalNonlinearity = "linear"
    analysis.addObject(solver)
    
    fea = ccxtools.FemToolsCcx()
    return fea



def run_solveur(fea):
    fea.purge_results()
    fea.run()


# Analyse of the results 
#fea.load_results()

def extract_deplacement():
    resultat = None
    for m in analysis.Group:
        if m.isDerivedFrom('Fem::FemResultObject'):
            resultat = m
            break
    if not resultat:
        raise Exception("aucun resultat n'a été trouver c'est triste")
    
    
    #min_deplacement = {"x":float("inf"), "y":float("inf"), "z":float("inf")}
    max_deplacement = {"x":-float("inf"), "y":-float("inf"), "z":-float("inf")}
    
    
    for vecteur in resultat.DisplacementVectors:      
        for k in max_deplacement.keys():
            deplacement = abs(getattr(vecteur, k))
            if deplacement > max_deplacement[k]:
                max_deplacement[k] = deplacement
         
            #if deplacement < min_deplacement[k]:
            #    min_deplacement[k] = deplacement
            
    #print(min_deplacement)
    #print(max_deplacement)
    return max_deplacement
    
#########################
#PRGM 
#########################

#""

model = create_3D_model("eprouvette_1.png", infill_height=10, bottom_height=0, top_height=0,  extrusion_thickness=0.5) # la valeur de infill height a été mise au pifométre

analysis = add_simulation()
compute_maillage(model)

traction_force = add_constraints(model, analysis,  1)

fea = add_solveur()


#l_charge = list(range(10, 2000, 50))
l_charge = [1000]

l_deplacement_x = []

for c in l_charge:
    traction_force.Force = c*1000 # / ! \ la force est en milli Newtonne donc on la mulitplie par mille
    run_solveur(fea)
    l_deplacement_x.append(extract_deplacement()["x"])


plt.clf()
plt.scatter(l_deplacement_x, l_charge)
plt.show()
