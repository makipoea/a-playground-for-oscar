import vtk

def read_vtk_file(filename):
    # Read the .vtk file
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    
    # Extract the unstructured grid
    unstructured_grid = reader.GetOutput()
    
    return unstructured_grid

def inspect_vtk_file(unstructured_grid):
    # Get the point data
    point_data = unstructured_grid.GetPointData()
    
    # Print the names of the arrays in the point data
    print("Point Data Arrays:")
    for i in range(point_data.GetNumberOfArrays()):
        array_name = point_data.GetArrayName(i)
        print(f"Array {i}: {array_name}")
    
    # Get the cell data (if needed)
    cell_data = unstructured_grid.GetCellData()
    
    # Print the names of the arrays in the cell data
    print("Cell Data Arrays:")
    for i in range(cell_data.GetNumberOfArrays()):
        array_name = cell_data.GetArrayName(i)
        print(f"Array {i}: {array_name}")

def main():
    filename = "poutre.vtk"  # Replace with your actual file path
    unstructured_grid = read_vtk_file(filename)
    inspect_vtk_file(unstructured_grid)

if __name__ == "__main__":
    main()
