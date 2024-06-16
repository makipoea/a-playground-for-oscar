import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import Axes3D

def read_vtk_file(filename):
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    
    unstructured_grid = reader.GetOutput()
    
    return unstructured_grid

def extract_stress_data(unstructured_grid, stress_array_name='von Mises Stress'):
    point_data = unstructured_grid.GetPointData()
    stress_array = point_data.GetArray(stress_array_name)
    
    if stress_array is None:
        raise ValueError(f"No stress data found in the file with the name '{stress_array_name}'.")
    
    stress_data = vtk_to_numpy(stress_array)
    points = vtk_to_numpy(unstructured_grid.GetPoints().GetData())
    
    return points, stress_data

def plot_stress_data(points, stress_data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    norm = Normalize(vmin=np.min(stress_data), vmax=np.max(stress_data))
    colors = plt.cm.viridis(norm(stress_data))
    
    scatter = ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=colors, marker='o')
    
    mappable = plt.cm.ScalarMappable(norm=norm, cmap='viridis')
    mappable.set_array(stress_data)
    fig.colorbar(mappable, ax=ax, label='Stress')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Internal Stress Distribution')
    
    plt.show()

def main():
    filename = 'poutre.vtk'
    unstructured_grid = read_vtk_file(filename)
    
    points, stress_data = extract_stress_data(unstructured_grid, stress_array_name='von Mises Stress')
    
    plot_stress_data(points, stress_data)

if __name__ == "__main__":
    main()
